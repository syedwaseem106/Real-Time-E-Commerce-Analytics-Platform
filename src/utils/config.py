import os
from dotenv import load_dotenv

# Load env variables from root level .env if it exists
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# PostgreSQL Configurations
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres123')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'ecommerce_warehouse')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Kafka Configurations
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(',')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'ecommerce_events')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'ecommerce-consumer-group')

# MinIO (S3) Configurations
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER', 'minioadmin')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin123')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://localhost:9000')
MINIO_BUCKET_RAW = os.getenv('MINIO_BUCKET_RAW', 'raw-events')
MINIO_BUCKET_PROCESSED = os.getenv('MINIO_BUCKET_PROCESSED', 'processed')
MINIO_BUCKET_EXPORTS = os.getenv('MINIO_BUCKET_EXPORTS', 'exports')

# Spark Configurations
SPARK_MASTER_URL = os.getenv('SPARK_MASTER_URL', 'local[*]')

def get_postgres_uri():
    """Returns SQLAlchemy connection URI for warehouse database"""
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_spark_config():
    """Returns a dictionary containing common Spark configurations"""
    return {
        "spark.master": SPARK_MASTER_URL,
        "spark.sql.streaming.forceDeleteTempCheckpointLocation": "true",
        "spark.hadoop.fs.s3a.endpoint": MINIO_ENDPOINT,
        "spark.hadoop.fs.s3a.access.key": MINIO_ROOT_USER,
        "spark.hadoop.fs.s3a.secret.key": MINIO_ROOT_PASSWORD,
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.connection.ssl.enabled": "false"
    }
