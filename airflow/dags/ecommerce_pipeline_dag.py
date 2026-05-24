# ==============================================================================
# APACHE AIRFLOW ORCHESTRATION DAG
# ==============================================================================

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import sys

# Ensure Airflow scheduler can import src modules
sys.path.append(os.getenv("AIRFLOW_HOME", "/opt/airflow"))

# Task Callables for PythonOperators
def run_event_generator():
    """Generates a transient batch of events and pushes directly to Kafka"""
    from src.event_generator.generator import EcommerceEventGenerator
    from src.event_generator.kafka_producer import EcommerceKafkaProducer
    
    print("Initiating transient event batch generation...")
    generator = EcommerceEventGenerator(num_users=200)
    batch = generator.generate_batch(count=300)
    
    print(f"Constructed {len(batch)} events. Publishing to Kafka topic...")
    producer = EcommerceKafkaProducer()
    producer.send_batch(batch)
    producer.close()
    print("Batch publishing completed successfully.")

def run_data_quality_checks():
    """Validates structural qualities inside PostgreSQL staging tables"""
    from sqlalchemy import create_engine, text
    from src.utils.config import get_postgres_uri
    
    engine = create_engine(get_postgres_uri())
    with engine.connect() as conn:
        res = conn.execute(text("SELECT COUNT(*) FROM staging.stg_events"))
        count = res.scalar()
        print(f"Staging area contains {count} events.")
        
        # Verify no negative values exist inside staging costs
        res_neg = conn.execute(text("SELECT COUNT(*) FROM staging.stg_events WHERE amount < 0"))
        negative_count = res_neg.scalar()
        if negative_count > 0:
            raise ValueError(f"Data Quality Error: Detected {negative_count} events with negative amounts!")
            
    print("Data quality checks passed successfully!")

def run_fact_loaders():
    """Triggers PostgreSQL warehouse star schema fact loaders"""
    from src.warehouse.load_facts import WarehouseFactLoader
    loader = WarehouseFactLoader()
    events, orders = loader.load_facts_from_staging()
    print(f"Successfully loaded {events} events and {orders} orders into fact tables.")

def run_analytics_exports():
    """Triggers CSV reports creation for downstream PowerBI/Tableau dashboards"""
    from src.analytics.export_csv import AnalyticsExporter
    from src.utils.config import get_postgres_uri
    
    exporter = AnalyticsExporter(get_postgres_uri(), export_dir="/opt/airflow/data/exports")
    exporter.export_all()
    print("CSV reports exported successfully.")

# Default DAG configuration parameters
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['alerts-de@company.com'],
    'email_on_failure': False, # Disabled locally to avoid connection errors
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(minutes=30),
}

with DAG(
    'ecommerce_analytics_pipeline',
    default_args=default_args,
    description='Production-style E-Commerce Batch + Stream Analytics Pipeline',
    schedule_interval='@hourly',
    start_date=days_ago(1),
    catchup=False,
    tags=['ecommerce', 'analytics', 'production'],
    max_active_runs=1,
) as dag:

    dag.doc_md = """
    ## E-Commerce Analytics Pipeline
    This DAG orchestrates our complete e-commerce pipeline on an hourly schedule:
    1. Asserts health of services (Kafka, Spark, Postgres).
    2. Simulates batch interactions by feeding events into Kafka.
    3. Runs PySpark batch processing to deduplicate click logs and store to Postgres staging.
    4. Validates structural quality of the staged records.
    5. Leverages **dbt** to build clean, documented user & product dim marts.
    6. Loads transactions into fact tables.
    7. Creates analytics views and exports flat CSV report dashboards.
    """

    # ==========================================
    # 1. HEALTH AND READINESS SENSORS
    # ==========================================
    check_kafka_health = BashOperator(
        task_id='check_kafka_health',
        bash_command='nc -z -v -w5 kafka 29092 || exit 1',
        retries=3,
        retry_delay=timedelta(seconds=10),
    )

    check_spark_health = BashOperator(
        task_id='check_spark_health',
        bash_command='nc -z -v -w5 spark-master 7077 || exit 1',
    )

    check_postgres_health = BashOperator(
        task_id='check_postgres_health',
        bash_command='nc -z -v -w5 postgres 5432 || exit 1',
    )

    # ==========================================
    # 2. INGESTION AND STREAM FEED
    # ==========================================
    generate_events = PythonOperator(
        task_id='generate_events',
        python_callable=run_event_generator,
    )

    # ==========================================
    # 3. SPARK TRANSFORMATIONS
    # ==========================================
    run_spark_batch = BashOperator(
        task_id='run_spark_batch',
        bash_command='spark-submit --packages org.postgresql:postgresql:42.6.0 /opt/airflow/src/spark/batch_processor.py',
    )

    # ==========================================
    # 4. QUALITY VALIDATIONS
    # ==========================================
    quality_checks = PythonOperator(
        task_id='quality_checks',
        python_callable=run_data_quality_checks,
    )

    # ==========================================
    # 5. DBT COMPILING AND SEEDING
    # ==========================================
    run_dbt_seed = BashOperator(
        task_id='run_dbt_seed',
        bash_command='cd /opt/airflow/dbt_project && dbt seed --profiles-dir . --target prod',
    )

    run_dbt_staging = BashOperator(
        task_id='run_dbt_staging',
        bash_command='cd /opt/airflow/dbt_project && dbt run --select staging --profiles-dir . --target prod',
    )

    run_dbt_marts = BashOperator(
        task_id='run_dbt_marts',
        bash_command='cd /opt/airflow/dbt_project && dbt run --select marts --profiles-dir . --target prod',
    )

    run_dbt_tests = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd /opt/airflow/dbt_project && dbt test --profiles-dir . --target prod',
    )

    # ==========================================
    # 6. SURROGATE KEY FACT LOADING
    # ==========================================
    load_fact_tables = PythonOperator(
        task_id='load_fact_tables',
        python_callable=run_fact_loaders,
    )

    # ==========================================
    # 7. ANALYTICAL LAYER EXPORTS
    # ==========================================
    create_reporting_views = PostgresOperator(
        task_id='create_reporting_views',
        postgres_conn_id='postgres_default',
        sql='src/analytics/create_views.sql',
    )

    export_dashboards = PythonOperator(
        task_id='export_dashboards',
        python_callable=run_analytics_exports,
    )

    # ==========================================
    # TASK LINEAGE CONFIGURATION
    # ==========================================
    [check_kafka_health, check_spark_health, check_postgres_health] >> generate_events
    generate_events >> run_spark_batch
    run_spark_batch >> quality_checks
    quality_checks >> run_dbt_seed
    run_dbt_seed >> run_dbt_staging
    run_dbt_staging >> run_dbt_marts
    run_dbt_marts >> run_dbt_tests
    run_dbt_tests >> load_fact_tables
    load_fact_tables >> create_reporting_views
    create_reporting_views >> export_dashboards
