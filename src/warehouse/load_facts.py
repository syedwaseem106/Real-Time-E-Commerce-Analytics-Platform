import sys
import time
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from src.warehouse.models import get_engine, FactEvent, FactOrder, DimUser, DimProduct, DimTime
from src.utils.logger import get_logger, log_pipeline_metric

logger = get_logger("warehouse-fact-loader")

class WarehouseFactLoader:
    """
    Transforms raw clickstream logs stored in the staging schema
    and inserts them into the core warehouse dimensional fact tables.
    """
    def __init__(self, engine=None):
        self.engine = engine if engine else get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def load_facts_from_staging(self):
        """
        Executes highly optimized, idempotent SQL queries to map natural keys 
        (user_id, product_id, event_date) to surrogate keys (user_key, product_key, time_key) 
        and inserts the records into fact tables.
        """
        start_time = time.time()
        session = self.Session()
        
        try:
            # 1. First, dynamically register any unregistered users/products 
            # to guarantee referential integrity (SCD Type 1 fallback)
            logger.info("Resolving late-arriving dimensions...")
            
            # Register late users
            register_users_query = """
            INSERT INTO warehouse.dim_users (user_id, username, email, segment, first_seen_date, last_seen_date, created_at, updated_at)
            SELECT DISTINCT 
                s.user_id, 
                COALESCE(s.username, 'Anonymous'), 
                COALESCE(s.email, 'anonymous@example.com'), 
                'regular', 
                s.event_date, 
                s.event_date,
                s.event_timestamp,
                s.event_timestamp
            FROM staging.stg_events s
            LEFT JOIN warehouse.dim_users u ON s.user_id = u.user_id
            WHERE u.user_key IS NULL AND s.user_id IS NOT NULL;
            """
            
            # Register late products
            register_products_query = """
            INSERT INTO warehouse.dim_products (product_id, product_name, category, subcategory, brand, base_price, created_at, updated_at)
            SELECT DISTINCT 
                s.product_id, 
                COALESCE(s.product_name, 'Unknown Product'), 
                COALESCE(s.category, 'Unknown Category'), 
                'Premium Category', 
                'Generic', 
                COALESCE(s.amount, 10.00),
                s.event_timestamp,
                s.event_timestamp
            FROM staging.stg_events s
            LEFT JOIN warehouse.dim_products p ON s.product_id = p.product_id
            WHERE p.product_key IS NULL AND s.product_id IS NOT NULL;
            """
            
            session.execute(text(register_users_query))
            session.execute(text(register_products_query))
            session.commit()
            logger.info("Dimension resolution completed.")

            # 2. Populate fact_events
            logger.info("Loading atomic events into warehouse.fact_events...")
            
            load_events_query = """
            INSERT INTO warehouse.fact_events (
                event_id, user_key, product_key, time_key, 
                session_id, event_type, amount, quantity, 
                device, browser, event_timestamp
            )
            SELECT DISTINCT
                s.event_id,
                u.user_key,
                p.product_key,
                t.time_key,
                s.session_id,
                s.event_type,
                s.amount,
                s.quantity,
                s.device,
                s.browser,
                s.event_timestamp
            FROM staging.stg_events s
            INNER JOIN warehouse.dim_users u ON s.user_id = u.user_id
            INNER JOIN warehouse.dim_products p ON s.product_id = p.product_id
            INNER JOIN warehouse.dim_time t ON s.event_date = t.full_date
            LEFT JOIN warehouse.fact_events f ON s.event_id = f.event_id
            WHERE f.event_key IS NULL; -- Prevent duplicates (idempotency check)
            """
            
            res_events = session.execute(text(load_events_query))
            events_loaded = res_events.rowcount
            logger.info(f"Successfully loaded {events_loaded} new records into fact_events.")

            # 3. Populate fact_orders
            logger.info("Extracting transactions into warehouse.fact_orders...")
            
            load_orders_query = """
            INSERT INTO warehouse.fact_orders (
                event_id, user_key, product_key, time_key, 
                session_id, order_amount, quantity, 
                device, browser, order_timestamp
            )
            SELECT DISTINCT
                s.event_id,
                u.user_key,
                p.product_key,
                t.time_key,
                s.session_id,
                s.amount,
                COALESCE(s.quantity, 1),
                s.device,
                s.browser,
                s.event_timestamp
            FROM staging.stg_events s
            INNER JOIN warehouse.dim_users u ON s.user_id = u.user_id
            INNER JOIN warehouse.dim_products p ON s.product_id = p.product_id
            INNER JOIN warehouse.dim_time t ON s.event_date = t.full_date
            LEFT JOIN warehouse.fact_orders fo ON s.event_id = fo.event_id
            WHERE s.event_type IN ('purchase', 'payment') 
              AND fo.order_key IS NULL; -- Prevent duplicates
            """
            
            res_orders = session.execute(text(load_orders_query))
            orders_loaded = res_orders.rowcount
            logger.info(f"Successfully loaded {orders_loaded} transactions into fact_orders.")

            # 4. Truncate staging table to prepare for next batch execution
            logger.info("Truncating staging area (staging.stg_events)...")
            session.execute(text("TRUNCATE TABLE staging.stg_events;"))
            session.commit()
            logger.info("Staging table purged.")
            
            duration = time.time() - start_time
            log_pipeline_metric(
                logger,
                pipeline_name="warehouse_load",
                step="stage_to_warehouse_facts",
                row_count=events_loaded,
                duration_seconds=duration,
                status="SUCCESS"
            )
            return events_loaded, orders_loaded

        except Exception as e:
            logger.error(f"Fact tables load transaction failed: {e}", exc_info=True)
            session.rollback()
            log_pipeline_metric(
                logger,
                pipeline_name="warehouse_load",
                step="stage_to_warehouse_facts",
                row_count=0,
                status="FAILED",
                error=e
            )
            return 0, 0
        finally:
            session.close()

def main():
    loader = WarehouseFactLoader()
    events, orders = loader.load_facts_from_staging()
    print(f"Fact loading completed. Events: {events}, Orders: {orders}")

if __name__ == '__main__':
    main()
