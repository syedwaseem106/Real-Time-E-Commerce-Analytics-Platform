import os
import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from src.utils.config import get_spark_config, MINIO_BUCKET_RAW, MINIO_BUCKET_PROCESSED, get_postgres_uri
from src.utils.logger import get_logger, log_pipeline_metric

logger = get_logger("spark-batch-processor")

def create_spark_session(app_name="EcommerceBatchProcessor"):
    """Creates SparkSession configured with postgres driver and S3 connections."""
    spark_conf = get_spark_config()
    builder = SparkSession.builder.appName(app_name)
    
    for key, val in spark_conf.items():
        builder = builder.config(key, val)
        
    builder = builder.config("spark.jars.packages", "org.postgresql:postgresql:42.6.0,org.apache.hadoop:hadoop-aws:3.3.4")
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

def process_daily_batch(spark, raw_path, processed_path, target_date=None):
    """
    Reads partitioned Parquet files for a given date, deduplicates them,
    computes aggregations, and saves the cleaned dataset.
    """
    start_time = datetime.now()
    
    # default to current date if none specified
    if not target_date:
        target_date = datetime.utcnow().strftime("%Y-%m-%d")
        
    logger.info(f"Initiating batch processing for target date: {target_date}")
    
    # 1. Read raw events for target date partition
    # Check if raw files exist
    partition_path = f"{raw_path}/event_date={target_date}"
    
    if not os.path.exists(partition_path) and not raw_path.startswith("s3a://"):
        # Local system check: create sample directory if missing to avoid crashes
        os.makedirs(partition_path, exist_ok=True)
        logger.warning(f"Partition directory {partition_path} was missing locally. Created blank.")
        return 0
        
    try:
        # Load parquet files
        df = spark.read.parquet(partition_path)
        raw_count = df.count()
        logger.info(f"Loaded {raw_count} raw records from date partition: {target_date}")
        
        if raw_count == 0:
            logger.warning(f"No records found for date: {target_date}")
            return 0
            
        # 2. Deduplicate records on event_id (ensure pipeline idempotence)
        deduped_df = df.dropDuplicates(["event_id"])
        deduped_count = deduped_df.count()
        duplicates_removed = raw_count - deduped_count
        logger.info(f"Deduplication completed. Extracted {deduped_count} unique events (removed {duplicates_removed} duplicates).")
        
        # 3. Add derived columns
        processed_df = deduped_df.withColumn("processed_at", F.current_timestamp())
        
        # 4. Save clean processed Parquet files back to Lake
        target_processed_path = f"{processed_path}/date={target_date}"
        logger.info(f"Writing clean Parquet dataset to: {target_processed_path}")
        processed_df.write \
            .mode("overwrite") \
            .parquet(target_processed_path)
            
        # 5. Load to staging table in PostgreSQL Warehouse
        postgres_uri = get_postgres_uri()
        db_properties = {
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", "postgres123"),
            "driver": "org.postgresql.Driver"
        }
        
        # Write to staging.stg_events
        # We rename columns to align with DB staging definition
        db_df = processed_df.select(
            F.col("event_id"),
            F.col("user_id"),
            F.col("session_id"),
            F.col("event_type"),
            F.col("product_id"),
            F.col("product_name"),
            F.col("category"),
            F.col("amount").cast("decimal(10,2)"),
            F.col("quantity").cast("integer"),
            F.col("device"),
            F.col("browser"),
            F.col("city"),
            F.col("country"),
            F.col("timestamp").cast("timestamp"),
            F.lit(target_date).cast("date").alias("event_date")
        )
        
        logger.info(f"Loading {deduped_count} staging events into PostgreSQL (staging.stg_events)")
        db_df.write \
            .jdbc(url=postgres_uri, table="staging.stg_events", mode="append", properties=db_properties)
            
        duration = (datetime.now() - start_time).total_seconds()
        log_pipeline_metric(
            logger, 
            pipeline_name="spark_batch_processing", 
            step="clean_and_stage", 
            row_count=deduped_count,
            duration_seconds=duration,
            status="SUCCESS"
        )
        return deduped_count
        
    except Exception as e:
        logger.error(f"Error executing daily batch process: {e}", exc_info=True)
        log_pipeline_metric(
            logger, 
            pipeline_name="spark_batch_processing", 
            step="clean_and_stage", 
            row_count=0,
            status="FAILED",
            error=e
        )
        return 0

def main():
    spark = None
    try:
        spark = create_spark_session()
        
        # Resolve storage locations
        raw_path = f"s3a://{MINIO_BUCKET_RAW}/events"
        processed_path = f"s3a://{MINIO_BUCKET_PROCESSED}/clean_events"
        
        if "localhost" in os.getenv("MINIO_ENDPOINT", "localhost"):
            raw_path = "./data/raw-events"
            processed_path = "./data/processed"
            
        # Support passing target date via arguments
        target_date = sys.argv[1] if len(sys.argv) > 1 else None
        
        process_daily_batch(spark, raw_path, processed_path, target_date)
        
    except Exception as e:
        logger.error(f"Batch processor main method crashed: {e}")
        sys.exit(1)
    finally:
        if spark:
            spark.stop()

if __name__ == '__main__':
    main()
