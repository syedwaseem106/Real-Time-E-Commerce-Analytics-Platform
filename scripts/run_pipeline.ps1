# ==============================================================================
# POWERSHELL PIPELINE RUNNER FOR WINDOWS
# ==============================================================================

Write-Host "======================================================" -ForegroundColor Blue
Write-Host "⚙️ Executing Data Pipeline Integration Workflow" -ForegroundColor Blue
Write-Host "======================================================" -ForegroundColor Blue

# 1. Start Spark Structured Streaming Consumer job in the background
Write-Host "Submitting PySpark Structured Streaming job to cluster..." -ForegroundColor Green
docker compose exec -d spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.4 /app/src/spark/streaming_consumer.py
Write-Host "Spark streaming job successfully submitted in background." -ForegroundColor Green

# 2. Trigger Event Generator to publish clickstream to Kafka
Write-Host "Launching simulated Faker event streams..." -ForegroundColor Green
docker compose exec -d spark-master python /app/src/event_generator/kafka_producer.py

Write-Host "Allowing streaming pipeline to run for 30 seconds to capture events..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Stop event publisher safely by killing its process in the spark container
Write-Host "Stopping event streaming..." -ForegroundColor Green
$containerId = docker ps --filter "name=spark-master" --format "{{.ID}}"
if ($containerId) {
    # Find the python process running kafka_producer
    $pids = docker exec -i spark-master ps aux | grep "kafka_producer.py" | awk '{print $2}'
    foreach ($pid in $pids) {
        if ($pid) {
            docker exec -d spark-master kill -9 $pid 2>$null
        }
    }
}
Write-Host "Event generator stopped. Stream ingest phase completed." -ForegroundColor Green

# 3. Trigger Batch Deduplication and PostgreSQL Staging loader
Write-Host "Executing Spark Batch Processor (Deduplication & staging)..." -ForegroundColor Green
docker compose exec -T spark-master spark-submit --packages org.postgresql:postgresql:42.6.0,org.apache.hadoop:hadoop-aws:3.3.4 /app/src/spark/batch_processor.py

# 4. Trigger dbt compilation, seeding, running staging and marts models, and tests
Write-Host "Executing dbt core models and quality assertions..." -ForegroundColor Green
docker compose exec -T airflow-webserver bash -c "cd /opt/airflow/dbt_project && dbt seed --profiles-dir . --target prod && dbt run --profiles-dir . --target prod && dbt test --profiles-dir . --target prod"

# 5. Execute Surrogate Key Fact Ingestion
Write-Host "Updating warehouse Fact Tables with staged records..." -ForegroundColor Green
docker compose exec -T spark-master python /app/src/warehouse/load_facts.py

# 6. Execute BI views creation and analytics reports CSV extraction
Write-Host "Creating analytical reporting views and exporting CSVs..." -ForegroundColor Green
docker compose exec -T spark-master python /app/src/analytics/export_csv.py

Write-Host "======================================================" -ForegroundColor Blue
Write-Host "🎉 Pipeline execution completed successfully!" -ForegroundColor Green
Write-Host "Dumped analytical reports ready inside data/exports/" -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Blue
