# 🚀 Real-Time E-Commerce Analytics Data Engineering Platform

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-7.5.0-orange.svg?style=for-the-badge&logo=apachekafka)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.0-red.svg?style=for-the-badge&logo=apachespark)](https://spark.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-green.svg?style=for-the-badge&logo=apacheairflow)](https://airflow.apache.org/)
[![dbt Core](https://img.shields.io/badge/dbt%20Core-1.7-purple.svg?style=for-the-badge&logo=dbt)](https://www.getdbt.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Blue.svg?style=for-the-badge&logo=docker)](https://www.docker.com/)

A production-style, locally runnable hybrid **Batch + Streaming Data Engineering Platform** simulating real-world e-commerce clickstream activities. This end-to-end pipeline simulates, ingests, processes, partitions, structures, orchestrates, models, and analyzes high-velocity click stream transactions to generate premium business reports.

---

## 📊 End-to-End System Architecture

```
[User Event Generator]
          ↓ (JSON Events)
   [Kafka Producer]
          ↓ (Linger & Gzip Compression)
    [Kafka Broker] (Topic: ecommerce_events | 3 Partitions)
          ↓ (Subscribe)
[Spark Structured Streaming] (Watermarking, Filtering)
          ↓ (Clean partitioned Parquet)
   [MinIO Data Lake] (raw-events bucket on local S3)
          ↓ (Hourly Scheduled Read)
[Spark Batch Deduplication] (dropDuplicates)
          ↓ (JDBC Bulk Load)
[PostgreSQL Staging] (staging.stg_events)
          ↓ (dbt Staging Models & Custom Macros)
    [dbt Marts] (SCD classifications, User Aggregates)
          ↓ (Surrogate Key Resolution Join)
[PostgreSQL Warehouse] (Star Schema dimensional facts)
          ↓ (Analytical Reporting Views)
[PostgreSQL Views] (analytics.v_reports)
          ↓ (Pandas CSV Extraction)
  [data/exports/] (Power BI/Tableau ready CSV reports)
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|---|---|---|---|
| **Programming** | Python, SQL | 3.10 | Core scripting and database query syntax. |
| **Ingestion Broker**| Apache Kafka, Zookeeper | 7.5.0 | High-velocity streaming commit log decoupling ingestion. |
| **Stream Processing**| PySpark Streaming | 3.5.0 | Consuming clickstreams and writing partitioned Parquet. |
| **Batch Processing**| PySpark SQL, JDBC | 3.5.0 | Deduplicating events hourly to maintain idempotence. |
| **Data Lake** | MinIO (S3-Compatible) | Latest | Local cloud storage staging raw/processed Parquet folders. |
| **Data Warehouse** | PostgreSQL | 15 | Relational OLAP Star Schema warehouse storage. |
| **Data Modeling** | dbt Core | 1.7.2 | Automated schema compilation, tests, and documentation. |
| **Orchestration** | Apache Airflow | 2.7.3 | Multi-stage DAG orchestration and execution schedules. |
| **Infrastructure** | Docker, Docker Compose | Latest | Standardized containerization for quick deployments. |

---

## 📁 Repository Structure

```
Real-Time E-Commerce Analytics Data Engineerin/
├── docker-compose.yml       # Primary Docker orchestration configuration
├── .env                     # Environmental credentials and port maps
├── .gitignore               # Ignored local environments and logs
├── Makefile                 # CLI shortcut bindings
├── requirements.txt         # Required Python packages
├── scripts/                 # Operational bash scripts
│   ├── setup.sh             # Deploys containers and seeds dimensions
│   ├── run_pipeline.sh      # Triggers local pipeline runs
│   └── teardown.sh          # Stops compose and resets directories
├── airflow/
│   ├── Dockerfile           # Custom Airflow container builder
│   └── dags/
│       └── ecommerce_pipeline_dag.py # Hourly orchestrator DAG
├── docker/
│   ├── spark/
│   │   └── Dockerfile       # PySpark image with MinIO connectors
│   ├── kafka/
│   │   └── init-topics.sh   # Creates Kafka primary and DLQ topics
│   └── postgres/
│       └── init.sql         # Seeds Postgres schemas
├── src/
│   ├── event_generator/     # Faker behavioral session simulations
│   │   ├── config.py        # Funnel distributions & catalog dictionary
│   │   ├── generator.py     # Clickstream event constructor
│   │   └── kafka_producer.py # Decoupled Kafka streaming publisher
│   ├── kafka/
│   │   └── consumer.py      # Diagnostic CLI consumer
│   ├── spark/
│   │   ├── transformations.py # Derived metrics and time dimensions
│   │   ├── streaming_consumer.py # Structured Streaming engine
│   │   └── batch_processor.py # Hourly deduplicator batch script
│   ├── warehouse/
│   │   ├── schema.sql       # Postgres Star DDL (PK, FK, Indexes)
│   │   ├── models.py        # SQLAlchemy mapping objects
│   │   ├── seed_dimensions.py # Generates 1000 users and dates
│   │   └── load_facts.py    # Surrogate keys fact loader script
│   ├── quality/
│   │   ├── validators.py    # Structural schemas and business rule tests
│   │   └── filters.py       # Deduplication and outlier cleanups
│   ├── analytics/
│   │   ├── queries.sql      # Portfolio of 15 advanced SQL queries
│   │   ├── create_views.sql # BI reporting views DDL
│   │   └── export_csv.py    # Pandas report exporter script
│   └── utils/
│       ├── logger.py        # Structured JSON logs utility
│       └── config.py        # Environment variables parser
├── dbt_project/             # Complete dbt Core code directory
│   ├── dbt_project.yml      # Model compilation materializations
│   ├── profiles.yml         # Dev/Prod Postgres profiles
│   ├── models/
│   │   ├── staging/         # Cleaned staging views (stg_events, etc.)
│   │   ├── marts/           # Relational warehouse dimensions & summaries
│   │   └── schema.yml       # Models meta documents and test binds
│   ├── tests/               # Custom data assertions
│   ├── macros/              # Schema names and divide helper macros
│   └── seeds/               # Product catalogs and segments CSVS
├── data/
│   ├── sample/              # Sample JSON click streams and exports
│   └── exports/             # Output target folder of CSV BI summaries
├── docs/
│   ├── architecture.md      # Engineering system pathways
│   ├── interview_prep.md    # 14 interview Q&A study guide
│   └── resume_bullets.md    # Metrics-driven resume bullet points
└── tests/                   # Pytest test directory
```

---

## ⚡ Quick Start Instructions

Deploy and execute the entire containerized platform in 3 simple commands:

### Step 1: Pre-configurations
Ensure Docker Desktop is running and healthy on your system. 

### Step 2: Spin Up and Bootstrap
Run the setup script inside Git Bash or terminal:
```bash
./scripts/setup.sh
```
This script will build custom containers, spin up Zookeeper, Kafka, Postgres, MinIO, Spark, and Airflow, establish topics, create database schemas, and pre-seed dimensions (creating 1000 fake user accounts, date spines, and product catalogs).

### Step 3: Execute the Data Pipeline
Run the integration script:
```bash
./scripts/run_pipeline.sh
```
This script submits the Structured Streaming consumer, runs simulated click traffic, triggers Spark batch deduplications, builds staging/marts views via dbt Core, loads PostgreSQL surrogate fact keys, and generates CSV reports.

---

## 📈 Dashboard CSV Export Reports

Once `run_pipeline.sh` finishes, you can locate clean, aggregated data reports ready for Power BI or Tableau inside [data/exports/](file:///c:/Users/Syed%20Waseem/OneDrive/Desktop/DE%20Projects/Real-Time%20E-Commerce%20Analytics%20Data%20Engineerin/data/exports/):

* `executive_summary_report.csv` — Gross revenues, visits, transaction counts, and basket sizes.
* `daily_sales_report.csv` — Rollups of order volume, revenue totals, units, and day-over-day growth.
* `product_performance_report.csv` — Ordered item units, categories, views, and product-specific sales.
* `category_revenue_report.csv` — Combined revenue aggregates grouped by product categories.
* `user_segments_report.csv` — Spend analysis metrics segmented by user status (VIP, Regular, etc.).
* `conversion_funnel_report.csv` — Drop-off percentages through the browsing-to-payment funnel.
* `hourly_traffic_report.csv` — Active peak hours of the day.

---

## 🔍 Data Quality, Governance & Observability

Production data engineering requires strict quality assurance and telemetry. This platform implements:
* **Schema Validation & Typing:** Enforces that click payloads have required fields, non-null user keys, and correct transaction quantities.
* **Dead Letter Queue (DLQ):** Diverts corrupt or negative transactions to `ecommerce_events_dlq` to protect active pipelines.
* **Idempotency (At-Least-Once):** Employs daily Spark batch deduplication on `event_id` and database surrogate merges using SQL `LEFT JOIN` checks during loading, preventing duplicated metrics if runs overlap.
* **dbt Assertions:** Executes unique constraints, non-null validators, accepted values, and referential checks across staging and dimensional tables.
* **Observability (JSON logging):** Employs structured JSON logs with timing execution tags (`pipeline_name`, `step`, `row_count`, `duration_seconds`) to monitor job health.

---

## 💼 Resume & Interview Ready

This project is explicitly modeled to help you clear technical challenges and architectural design rounds at tier-1 cloud and product companies:
* **ATS Resume Points:** Copy and adapt metrics-driven resume bullets located inside [docs/resume_bullets.md](file:///c:/Users/Syed%20Waseem/OneDrive/Desktop/DE%20Projects/Real-Time%20E-Commerce%20Analytics%20Data%20Engineerin/docs/resume_bullets.md).
* **Technical Question Vault:** Study comprehensive explanations regarding watermarking, idempotence, star schemas, partition strategies, and scaling to 100x volume inside [docs/interview_prep.md](file:///c:/Users/Syed%20Waseem/OneDrive/Desktop/DE%20Projects/Real-Time%20E-Commerce%20Analytics%20Data%20Engineerin/docs/interview_prep.md).
* **System Diagrams:** Check clean system design workflows and Kimball diagrams inside [docs/architecture.md](file:///c:/Users/Syed%20Waseem/OneDrive/Desktop/DE%20Projects/Real-Time%20E-Commerce%20Analytics%20Data%20Engineerin/docs/architecture.md).

---

## 📄 License & Contributions

Licensed under the MIT License. Contributions and PRs are welcome!
