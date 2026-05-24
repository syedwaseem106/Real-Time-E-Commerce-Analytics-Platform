FROM bitnami/spark:3.5

USER root

# Install python dependencies
RUN pip install --no-cache-dir \
    kafka-python==2.0.2 \
    boto3==1.34.0 \
    psycopg2-binary==2.9.9 \
    sqlalchemy==2.0.23 \
    faker==22.0.0 \
    pandas==2.1.4 \
    python-dotenv==1.0.0

# Add jar files for S3/MinIO and Kafka integration
# Spark 3.5 requires hadoop-aws-3.3.4.jar and aws-java-sdk-bundle-1.12.262.jar or similar
RUN mkdir -p /opt/bitnami/spark/jars && \
    curl -o /opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -o /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.262.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

WORKDIR /app
COPY ./src /app/src

USER 1001
