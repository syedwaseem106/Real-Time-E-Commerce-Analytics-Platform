#!/usr/bin/env bash
# ==============================================================================
# E-COMMERCE ANALYTICS PLATFORM - PIPELINE RUNNER
# ==============================================================================

set -eo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}⚙️ Executing Data Pipeline Integration Workflow${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Start Spark Structured Streaming Consumer job in the background
echo -e "${GREEN}Submitting PySpark Structured Streaming job to cluster...${NC}"
docker compose exec -d spark-master spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.4 \
    /app/src/spark/streaming_consumer.py
echo -e "${GREEN}Spark streaming job successfully submitted in background.${NC}"

# 2. Trigger Event Generator to publish clickstream to Kafka
echo -e "${GREEN}Launching simulated Faker event streams...${NC}"
# We spin event streams in background for 30 seconds to simulate click flows
docker compose exec -d spark-master python /app/src/event_generator/kafka_producer.py &
PRODUCER_PID=$!

echo -e "${YELLOW}Allowing streaming pipeline to run for 30 seconds to capture events...${NC}"
sleep 30

# Stop event publisher safely
kill $PRODUCER_PID || true
echo -e "${GREEN}Event generator stopped. Stream ingest phase completed.${NC}"

# 3. Trigger Batch Deduplication and PostgreSQL Staging loader
echo -e "${GREEN}Executing Spark Batch Processor (Deduplication & staging)...${NC}"
docker compose exec -T spark-master spark-submit \
    --packages org.postgresql:postgresql:42.6.0,org.apache.hadoop:hadoop-aws:3.3.4 \
    /app/src/spark/batch_processor.py

# 4. Trigger dbt compilation, seeding, running staging and marts models, and tests
echo -e "${GREEN}Executing dbt core models and quality assertions...${NC}"
docker compose exec -T airflow-webserver bash -c "
    cd /opt/airflow/dbt_project && \
    dbt seed --profiles-dir . --target prod && \
    dbt run --profiles-dir . --target prod && \
    dbt test --profiles-dir . --target prod
"

# 5. Execute Surrogate Key Fact Ingestion
echo -e "${GREEN}Updating warehouse Fact Tables with staged records...${NC}"
docker compose exec -T spark-master python /app/src/warehouse/load_facts.py

# 6. Execute BI views creation and analytics reports CSV extraction
echo -e "${GREEN}Creating analytical reporting views and exporting CSVs...${NC}"
docker compose exec -T spark-master python /app/src/analytics/export_csv.py

echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}🎉 Pipeline execution completed successfully!${NC}"
echo -e "${YELLOW}Dumped analytical reports ready inside data/exports/${NC}"
echo -e "${BLUE}======================================================${NC}"
