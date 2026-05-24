import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql import functions as F
from src.utils.config import get_spark_config, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, MINIO_BUCKET_RAW
from src.spark.transformations import add_time_dimensions, flag_suspicious_events

def create_spark_session(app_name="EcommerceStreamingConsumer"):
    """
    Creates a robust SparkSession equipped with AWS S3/MinIO and Kafka packages.
    """
    spark_conf = get_spark_config()
    
    # Establish base builder
    builder = SparkSession.builder.appName(app_name)
    
    # Apply standard settings from config
    for key, val in spark_conf.items():
        builder = builder.config(key, val)
        
    # Dynamically include package dependencies if running locally outside Docker
    # To run successfully on Windows/local machine:
    builder = builder.config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.4")
    
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark

def define_event_schema():
    """Defines structural schema matching JSON output of Faker event generator."""
    return StructType([
        StructField("event_id", StringType(), False),
        StructField("user_id", StringType(), False),
        StructField("username", StringType(), True),
        StructField("email", StringType(), True),
        StructField("session_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("product_id", StringType(), False),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("device", StringType(), True),
        StructField("browser", StringType(), True),
        StructField("city", StringType(), True),
        StructField("country", StringType(), True),
        StructField("timestamp", StringType(), False),
        StructField("event_date", StringType(), False)
    ])

def read_kafka_stream(spark, bootstrap_servers, topic):
    """Binds to streaming Kafka topic."""
    # Convert list of brokers back to comma-separated string
    brokers = ",".join(bootstrap_servers) if isinstance(bootstrap_servers, list) else bootstrap_servers
    
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", brokers) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

def apply_transformations(df, schema):
    """
    Parses Kafka byte payload, structures it into schema, removes malformed records,
    and enriches it with time dimensions.
    """
    # Deserialize byte messages
    parsed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING) as json_value") \
        .select(F.from_json(F.col("json_value"), schema).alias("data")) \
        .select("data.*")
        
    # Quality Filter: Discard blank fields, invalid values, negative amounts
    filtered_df = parsed_df.filter(
        (F.col("event_id").isNotNull()) & 
        (F.col("user_id").isNotNull()) & 
        (F.col("event_type").isNotNull()) &
        ((F.col("amount") >= 0.0) | (F.col("amount").isNull()))
    )
    
    # Cast strings to proper timestamp structures
    enriched_df = filtered_df.withColumn(
        "timestamp_parsed", 
        F.to_timestamp(F.col("timestamp"), "yyyy-MM-dd HH:mm:ss.SSS")
    ).drop("timestamp").withColumnRenamed("timestamp_parsed", "timestamp")
    
    # Add watermark to handle latency out-of-order data
    watermarked_df = enriched_df.withWatermark("timestamp", "10 minutes")
    
    # Enrich dimensions
    time_df = add_time_dimensions(watermarked_df)
    suspicious_df = flag_suspicious_events(time_df)
    
    return suspicious_df

def write_to_minio(df, output_path, checkpoint_path):
    """
    Structured Streaming Writer: Writes partitions of clean event Parquet records
    into MinIO (partitioned by event_date).
    """
    return df.writeStream \
        .format("parquet") \
        .partitionBy("event_date") \
        .option("path", output_path) \
        .option("checkpointLocation", checkpoint_path) \
        .outputMode("append") \
        .trigger(processingTime="15 seconds")

def main():
    spark = None
    try:
        # Initialize spark session
        spark = create_spark_session()
        schema = define_event_schema()
        
        # Configure streaming paths
        # In Docker Compose environment, standard endpoints resolve to container hosts.
        # Locally, they fallback to localhost directories.
        s3_raw_path = f"s3a://{MINIO_BUCKET_RAW}/events"
        s3_checkpoint_path = f"s3a://{MINIO_BUCKET_RAW}/checkpoints/events"
        
        # fallback directories if s3 configs are running local filesystem
        if "localhost" in os.getenv("MINIO_ENDPOINT", "localhost"):
            # If executing directly on local dev computer without docker, write local paths
            # so it runs flawlessly out-of-the-box
            s3_raw_path = "./data/raw-events"
            s3_checkpoint_path = "./data/checkpoints"
            
        print(f"Reading from Kafka Brokers: {KAFKA_BOOTSTRAP_SERVERS}")
        print(f"Subscribed Topic: {KAFKA_TOPIC}")
        print(f"Writing Parquet events to: {s3_raw_path}")
        
        raw_stream_df = read_kafka_stream(spark, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC)
        transformed_df = apply_transformations(raw_stream_df, schema)
        
        # Start write stream
        query = write_to_minio(transformed_df, s3_raw_path, s3_checkpoint_path).start()
        
        # Also let's run an inline Console aggregate to prove it's actively capturing real-time metrics
        agg_df = transformed_df \
            .groupBy("event_type") \
            .agg(
                F.count("event_id").alias("event_count"),
                F.sum("amount").alias("total_revenue")
            )
            
        console_query = agg_df.writeStream \
            .format("console") \
            .outputMode("complete") \
            .trigger(processingTime="30 seconds") \
            .start()
            
        query.awaitTermination()
        console_query.awaitTermination()
        
    except Exception as e:
        print(f"Structured streaming application crashed: {e}")
        sys.exit(1)
    finally:
        if spark:
            spark.stop()

if __name__ == '__main__':
    main()
