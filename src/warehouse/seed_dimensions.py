import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import sessionmaker
from src.warehouse.models import get_engine, DimUser, DimProduct, DimTime
from src.event_generator.config import PRODUCTS, CATEGORIES
from src.utils.logger import get_logger

logger = get_logger("warehouse-seeder")

def seed_time_dimension(session, start_date_str="2024-01-01", end_date_str="2026-12-31"):
    """
    Pre-populates the time dimension (dim_time) to enable optimized e-commerce
    time-intelligence aggregations (YoY, MoM, Weekend performance).
    """
    logger.info(f"Seeding DimTime from {start_date_str} to {end_date_str}...")
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    
    # Check if dim_time is already populated
    existing_count = session.query(DimTime).count()
    if existing_count > 0:
        logger.info(f"DimTime already seeded with {existing_count} records. Skipping.")
        return
        
    delta = timedelta(days=1)
    current_date = start_date
    records = []
    
    while current_date <= end_date:
        is_wk = current_date.weekday() in [5, 6] # Saturday=5, Sunday=6
        
        dim_t = DimTime(
            full_date=current_date,
            year=current_date.year,
            quarter=(current_date.month - 1) // 3 + 1,
            month=current_date.month,
            month_name=current_date.strftime("%B"),
            week_of_year=current_date.isocalendar()[1],
            day_of_month=current_date.day,
            day_of_week=current_date.weekday() + 1, # 1-indexed (Mon=1)
            day_name=current_date.strftime("%A"),
            is_weekend=is_wk,
            is_holiday=False, # Could integrate holidays API if desired
            fiscal_year=current_date.year,
            fiscal_quarter=(current_date.month - 1) // 3 + 1
        )
        records.append(dim_t)
        current_date += delta
        
        # Batch insert to avoid bottlenecking
        if len(records) >= 500:
            session.bulk_save_objects(records)
            session.commit()
            records = []
            
    if records:
        session.bulk_save_objects(records)
        session.commit()
        
    total = session.query(DimTime).count()
    logger.info(f"Seeding DimTime complete. Total rows: {total}")

def seed_products_dimension(session):
    """Fills dim_products catalog using static configurations."""
    logger.info("Seeding DimProducts catalog...")
    
    existing_count = session.query(DimProduct).count()
    if existing_count > 0:
        logger.info(f"DimProducts already populated with {existing_count} items. Skipping.")
        return
        
    now = datetime.utcnow()
    records = []
    
    for prod_id, info in PRODUCTS.items():
        # Derive brand and subcategory from product descriptions to make it highly authentic
        words = info["name"].split()
        brand = words[0] if len(words) > 0 else "Generic"
        subcat = f"Premium {info['category']}"
        
        dim_p = DimProduct(
            product_id=prod_id,
            product_name=info["name"],
            category=info["category"],
            subcategory=subcat,
            brand=brand,
            base_price=info["base_price"],
            is_active=True,
            created_at=now,
            updated_at=now
        )
        records.append(dim_p)
        
    session.bulk_save_objects(records)
    session.commit()
    logger.info(f"Seeding DimProducts complete. Seeded {len(PRODUCTS)} products.")

def seed_users_dimension(session, num_users=1000):
    """Pre-seeds dim_users using Faker to create high-quality historical customer records."""
    logger.info(f"Seeding DimUsers database with {num_users} users...")
    
    existing_count = session.query(DimUser).count()
    if existing_count > 0:
        logger.info(f"DimUsers already loaded with {existing_count} records. Skipping.")
        return
        
    faker = Faker()
    devices = ['mobile', 'desktop', 'tablet']
    now = datetime.utcnow()
    records = []
    
    for i in range(num_users):
        # Establish realistic user signup timelines over the past year
        signup_offset = random.randint(10, 365)
        signup_date = now - timedelta(days=signup_offset)
        last_active = signup_date + timedelta(days=random.randint(0, signup_offset))
        
        dim_u = DimUser(
            user_id=f"usr_{faker.unique.uuid4().hex[:10]}",
            username=faker.user_name(),
            email=faker.email(),
            city=faker.city(),
            country=faker.country(),
            device_preference=random.choice(devices),
            segment=random.choice(['regular', 'VIP', 'bargain_hunter', 'frequent_buyer']),
            first_seen_date=signup_date.date(),
            last_seen_date=last_active.date(),
            is_active=random.choices([True, False], weights=[90, 10])[0],
            created_at=signup_date,
            updated_at=last_active
        )
        records.append(dim_u)
        
        if len(records) >= 500:
            session.bulk_save_objects(records)
            session.commit()
            records = []
            
    if records:
        session.bulk_save_objects(records)
        session.commit()
        
    total = session.query(DimUser).count()
    logger.info(f"Seeding DimUsers complete. Loaded {total} total user records.")

def main():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        seed_time_dimension(session)
        seed_products_dimension(session)
        seed_users_dimension(session, num_users=1000)
        logger.info("Database seeding process completed successfully!")
    except Exception as e:
        logger.error(f"Error during dimension seeding: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    main()
