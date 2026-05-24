# ==============================================================================
# MAKEFILE FOR E-COMMERCE DATA ENGINEERING PLATFORM
# ==============================================================================

.PHONY: up down restart logs ps clean status kafka-topics generate-events spark-submit dbt-run dbt-test dbt-seed psql

up:
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose down && docker compose up -d --build

logs:
	docker compose logs -f

ps:
	docker compose ps

status:
	docker compose ps

kafka-topics:
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

generate-events:
	python src/event_generator/kafka_producer.py

spark-submit-streaming:
	docker compose exec spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /app/src/spark/streaming_consumer.py

spark-submit-batch:
	docker compose exec spark-master spark-submit /app/src/spark/batch_processor.py

dbt-seed:
	cd dbt_project && dbt seed --profiles-dir .

dbt-run:
	cd dbt_project && dbt run --profiles-dir .

dbt-test:
	cd dbt_project && dbt test --profiles-dir .

psql:
	docker compose exec postgres psql -U postgres -d ecommerce_warehouse

clean:
	docker compose down -v --rmi all
