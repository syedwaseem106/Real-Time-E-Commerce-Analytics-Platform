
<div align="center">

# ⚡ Real-Time E-Commerce Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Kafka-7.5.0-231F20?style=for-the-badge&logo=apachekafka&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Spark-3.5.0-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Airflow-2.7-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/dbt_Core-1.7-FF694B?style=for-the-badge&logo=dbt&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/MinIO-S3_Compatible-C72E49?style=for-the-badge&logo=minio&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

<p align="center">
  <b>Production-grade hybrid Batch + Streaming data engineering platform simulating real-world e-commerce clickstream events.</b><br/>
  <i>End-to-end pipeline — Event Generation → Kafka → Spark → MinIO Data Lake → PostgreSQL → dbt → BI Exports</i>
</p>

<p align="center">
  <a href="#-pipeline-architecture">Architecture</a> •
  <a href="#-platform-at-a-glance">Metrics</a> •
  <a href="#️-tech-stack">Tech Stack</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-data-model--star-schema">Data Model</a> •
  <a href="#-engineering-decisions">Engineering Decisions</a>
</p>

</div>

---

## 🏗️ Pipeline Architecture

![Pipeline Architecture]<img width="712" height="643" alt="Screenshot 2026-05-24 175154" src="https://github.com/user-attachments/assets/c37c9757-76bf-4276-b170-416708b5408c" />


```
┌──────────────────────────────────────────────────────────────────────┐
│                        EVENT GENERATION LAYER                        │
│                                                                      │
│   Faker-based Behavioral Simulator                                   │
│   ├── 1,000 synthetic users with segment profiles (VIP/Regular/New) │
│   ├── Funnel-weighted event distribution                             │
│   │     page_view → add_to_cart → checkout → purchase               │
│   └── JSON event payload → Kafka Producer (Linger + GZip batch)     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    Kafka Broker (Confluent 7.5.0)
              Topic: ecommerce_events  |  3 partitions
              DLQ:   ecommerce_events_dlq  (corrupt / invalid events)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                     STREAM PROCESSING LAYER                          │
│                                                                      │
│   PySpark Structured Streaming (3.5.0)                               │
│   ├── Event-time watermarking (late arrival tolerance)               │
│   ├── Schema validation — invalid events → DLQ topic                 │
│   ├── Derived metrics:                                               │
│   │     engagement_score · funnel_stage · session_duration           │
│   └── Partitioned Parquet write → MinIO data lake                   │
│         Partition: year= / month= / day= / hour=                     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
              MinIO S3-Compatible Data Lake (raw-events/)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                      BATCH PROCESSING LAYER                          │
│                                                                      │
│   PySpark SQL + JDBC (hourly, triggered by Airflow)                  │
│   ├── dropDuplicates on event_id (idempotent re-run safe)            │
│   └── JDBC bulk load → PostgreSQL staging.stg_events                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                PostgreSQL → staging.stg_events
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    TRANSFORMATION LAYER  (dbt Core 1.7)              │
│                                                                      │
│   Staging Models              Mart Models            Seeds           │
│   ├── stg_events              ├── dim_users           ├── products   │
│   ├── stg_users               ├── dim_products        └── segments   │
│   └── stg_products            ├── dim_date                           │
│                               ├── fct_events (SCD)                   │
│                               └── agg_user_summary                   │
│                                                                      │
│   Tests: unique · not_null · accepted_values · referential integrity │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    WAREHOUSE LAYER  (Star Schema)                    │
│                                                                      │
│   dim_users ──┐                                                      │
│   dim_products┼──► fct_events ◄── dim_date                          │
│   dim_segments┘         │                                            │
│                         └──► analytics.v_reports (15 SQL queries)   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                         REPORTING LAYER                              │
│                                                                      │
│   Pandas CSV Exporter → data/exports/ → Power BI / Tableau          │
│   7 business reports: executive · daily sales · products ·           │
│   categories · user segments · conversion funnel · hourly traffic   │
└──────────────────────────────────────────────────────────────────────┘

  Orchestration: Apache Airflow 2.7 — hourly 6-stage DAG with retry handling
  Infrastructure: Docker Compose — single-command full stack deployment
```

---

## 📊 Platform at a Glance

| Metric | Value |
|:--|:--|
| 👤 Simulated Users | 1,000 (VIP / Regular / New segments) |
| 📡 Event Types | `page_view` · `add_to_cart` · `checkout` · `purchase` · `session` |
| 🗂️ Kafka Partitions | 3 main + 1 Dead Letter Queue |
| 🗄️ Parquet Partitioning | `year / month / day / hour` |
| 🔧 dbt Models | Staging views + 4 mart models |
| 📁 BI CSV Reports | 7 Power BI / Tableau-ready exports |
| ⏰ Orchestration | Hourly 6-stage Airflow DAG |
| 🐳 Docker Services | 6 (Zookeeper, Kafka, Spark, PostgreSQL, MinIO, Airflow) |

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|:--|:--|:--|:--|
| **Language** | Python · SQL | 3.10 | Core pipeline scripting and analytics |
| **Message Broker** | Apache Kafka + Zookeeper | 7.5.0 | Decoupled high-velocity streaming commit log |
| **Stream Processing** | PySpark Structured Streaming | 3.5.0 | Real-time event consumption and Parquet writes |
| **Batch Processing** | PySpark SQL + JDBC | 3.5.0 | Hourly deduplication and warehouse loading |
| **Data Lake** | MinIO (S3-compatible) | Latest | Local cloud-style object storage for raw Parquet |
| **Data Warehouse** | PostgreSQL | 15 | Star schema OLAP relational storage |
| **Transformation** | dbt Core | 1.7.2 | Staging, mart models, tests, and lineage docs |
| **Orchestration** | Apache Airflow | 2.7.3 | Scheduled DAG execution, retries, monitoring |
| **Infrastructure** | Docker + Docker Compose | Latest | Fully containerized single-command deployment |

---

## ⚡ Quick Start

> **Prerequisites:** Docker Desktop · Git Bash or a Unix-compatible terminal

### 1. Clone the repository
```bash
git clone https://github.com/syedwaseem106/Real-Time-E-Commerce-Analytics-Platform.git
cd Real-Time-E-Commerce-Analytics-Platform
```

### 2. Bootstrap the full platform
```bash
./scripts/setup.sh
```
Builds all custom Docker images and spins up Zookeeper, Kafka, MinIO, Spark, PostgreSQL, and Airflow. Creates Kafka topics, initializes the database schema, and seeds 1,000 synthetic users, a 2024–2026 date spine, and the product catalog.

### 3. Run the end-to-end pipeline
```bash
./scripts/run_pipeline.sh
```
Launches Structured Streaming, generates clickstream traffic, runs Spark batch deduplication, executes dbt builds, loads surrogate fact keys into PostgreSQL, and exports all 7 BI reports to `data/exports/`.

---

## 🖥️ Service URLs

| Service | URL | Credentials |
|:--|:--|:--|
| 🌬️ Airflow UI | http://localhost:8080 | `airflow / airflow` |
| 🪣 MinIO Console | http://localhost:9001 | `minioadmin / minioadmin` |
| ⚡ Spark UI | http://localhost:4040 | — |
| 🐘 pgAdmin | http://localhost:5050 | `admin@admin.com / admin` |

---

## 📁 Project Structure

```
real-time-ecommerce-analytics/
│
├── docker-compose.yml               # Full 6-service orchestration
├── .env                             # Credentials and port configuration
├── Makefile                         # CLI shortcuts (make setup, make run, etc.)
├── requirements.txt                 # Python dependencies
│
├── scripts/
│   ├── setup.sh                     # Bootstrap all containers + seed data
│   ├── run_pipeline.sh              # End-to-end pipeline trigger
│   └── teardown.sh                  # Clean shutdown and volume reset
│
├── docker/
│   ├── spark/Dockerfile             # PySpark image with MinIO S3 connectors
│   ├── kafka/init-topics.sh         # Creates ecommerce_events + DLQ topics
│   └── postgres/init.sql            # PostgreSQL schema initialization
│
├── airflow/
│   ├── Dockerfile                   # Custom Airflow image
│   └── dags/
│       └── ecommerce_pipeline_dag.py  # 6-stage hourly orchestration DAG
│
├── src/
│   ├── event_generator/
│   │   ├── config.py                # Funnel distributions, product catalog
│   │   ├── generator.py             # Faker-based clickstream constructor
│   │   └── kafka_producer.py        # Kafka publisher with GZip batching
│   │
│   ├── spark/
│   │   ├── streaming_consumer.py    # Structured Streaming engine
│   │   ├── batch_processor.py       # Hourly deduplication Spark job
│   │   └── transformations.py       # Derived metrics, time dimensions
│   │
│   ├── warehouse/
│   │   ├── schema.sql               # PostgreSQL DDL (PKs, FKs, indexes)
│   │   ├── models.py                # SQLAlchemy ORM mappings
│   │   ├── seed_dimensions.py       # Seeds 1,000 users + date spine + products
│   │   └── load_facts.py            # Surrogate key resolution + fact load
│   │
│   ├── quality/
│   │   ├── validators.py            # Payload schema + business rule checks
│   │   └── filters.py               # Deduplication and outlier removal
│   │
│   └── analytics/
│       ├── queries.sql              # 15 advanced analytical SQL queries
│       ├── create_views.sql         # BI reporting view DDL
│       └── export_csv.py            # Pandas CSV export script
│
├── dbt_project/
│   ├── dbt_project.yml              # Materialization config
│   ├── profiles.yml                 # Dev/Prod PostgreSQL profiles
│   ├── models/
│   │   ├── staging/                 # stg_events, stg_users, stg_products
│   │   ├── marts/                   # dim_*, fct_events, agg_user_summary
│   │   └── schema.yml               # Model tests, docs, and metadata
│   ├── macros/                      # Custom Jinja macros
│   ├── tests/                       # Custom dbt data assertions
│   └── seeds/                       # Product catalog and segment CSVs
│
└── data/
    ├── sample/                      # Sample event JSON payloads
    └── exports/                     # BI-ready CSV output folder
```

---

## 🗄️ Data Model — Star Schema

### Dimension Tables

| Table | Key Columns | Description |
|:--|:--|:--|
| `dim_users` | `user_id (PK)`, `segment`, `created_at` | 1,000 synthetic users with VIP / Regular / New segments |
| `dim_products` | `product_id (PK)`, `category`, `price` | 50+ products across categories |
| `dim_date` | `date_id (PK)`, `year`, `month`, `week`, `day_of_week` | Full 2024–2026 date spine |
| `dim_segments` | `segment_id (PK)`, `segment_name`, `tier` | User tier classifications |

### Fact Table — `fct_events`

| Column | Type | Notes |
|:--|:--|:--|
| `event_id` | `VARCHAR (PK)` | Deduplicated unique event identifier |
| `user_id` | `INT (FK)` | Resolves to `dim_users` surrogate key |
| `product_id` | `INT (FK)` | Resolves to `dim_products` surrogate key |
| `date_id` | `INT (FK)` | Resolves to `dim_date` surrogate key |
| `event_type` | `VARCHAR` | `page_view` / `add_to_cart` / `checkout` / `purchase` |
| `session_id` | `VARCHAR` | Groups events into user sessions |
| `quantity` | `INT` | Units per transaction event |
| `revenue` | `DOUBLE PRECISION` | Derived: `quantity × product price` |
| `funnel_stage` | `INT` | 1–4 numeric funnel position |
| `created_at` | `TIMESTAMP` | Event timestamp with timezone |

---

## 📊 Sample Output — Conversion Funnel

> Result of running `src/analytics/queries.sql` against `fct_events`

| funnel_stage | event_type | event_count | funnel_pct |
|:--|:--|:--|:--|
| 1 | page_view | 98,432 | 100.00% |
| 2 | add_to_cart | 61,204 | 62.18% |
| 3 | checkout | 30,891 | 31.38% |
| 4 | purchase | 14,203 | 14.43% |

---

## 📈 BI Report Exports

After `run_pipeline.sh` completes, Power BI / Tableau-ready CSVs land in `data/exports/`:

| Report File | Description |
|:--|:--|
| `executive_summary_report.csv` | Gross revenue, visits, transaction counts, and basket sizes |
| `daily_sales_report.csv` | Order volume, daily revenue, units sold, and day-over-day growth |
| `product_performance_report.csv` | Units sold, views, and revenue per product |
| `category_revenue_report.csv` | Revenue aggregated by product category |
| `user_segments_report.csv` | Spend metrics segmented by user tier (VIP, Regular, New) |
| `conversion_funnel_report.csv` | Drop-off rates across browse → cart → checkout → payment |
| `hourly_traffic_report.csv` | Active session volume by hour of day |

---

## 🔍 SQL Analytics — Sample Query

15 analytical queries live in `src/analytics/queries.sql`, covering funnel drop-off, revenue by segment, hourly traffic peaks, product conversion rates, repeat purchase analysis, and day-over-day growth.

```sql
-- Conversion funnel drop-off analysis
SELECT
    funnel_stage,
    event_type,
    COUNT(*)                                             AS event_count,
    ROUND(
        100.0 * COUNT(*) / FIRST_VALUE(COUNT(*)) OVER (
            ORDER BY funnel_stage
        ), 2
    )                                                    AS funnel_pct
FROM fct_events
GROUP BY funnel_stage, event_type
ORDER BY funnel_stage;
```

---

## 🔒 Data Quality & Observability

| Practice | Implementation |
|:--|:--|
| **Schema Validation** | Enforces required fields, non-null user keys, and valid quantities on every Kafka event |
| **Dead Letter Queue** | Malformed or out-of-range events route to `ecommerce_events_dlq` — main pipeline stays clean |
| **Idempotency** | Spark deduplicates on `event_id`; fact loader uses `LEFT JOIN` guard to block duplicate inserts on re-run |
| **dbt Tests** | `unique`, `not_null`, `accepted_values`, and referential integrity tests on every model build |
| **Structured Logging** | JSON logs with `pipeline_name`, `step`, `row_count`, and `duration_seconds` on every job execution |

### dbt Test Results

| Test | Model | Column | Status |
|:--|:--|:--|:--|
| `unique` | `fct_events` | `event_id` | ✅ Passed |
| `not_null` | `fct_events` | `user_id` | ✅ Passed |
| `not_null` | `fct_events` | `product_id` | ✅ Passed |
| `accepted_values` | `fct_events` | `event_type` | ✅ Passed |
| `referential_integrity` | `fct_events` | `user_id → dim_users` | ✅ Passed |
| `referential_integrity` | `fct_events` | `product_id → dim_products` | ✅ Passed |

---

## 💡 Engineering Decisions

> See [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md) for full engineering rationale.

<details>
<summary><b>Why Kafka over writing directly to the database?</b></summary>

Kafka decouples producers from consumers, absorbs traffic spikes without data loss, and enables event replay for late arrivals or pipeline failures — critical for at-least-once delivery guarantees.
</details>

<details>
<summary><b>Why Parquet partitioned by time on MinIO?</b></summary>

Columnar Parquet with `year/month/day/hour` partitioning enables partition pruning in both Spark Streaming writes and hourly batch reads, cutting scan cost as data volume grows.
</details>

<details>
<summary><b>Why dbt for transformations instead of raw SQL scripts?</b></summary>

Version-controlled, testable, self-documenting models with full lineage graphs. Staging → mart separation mirrors how professional data teams manage transformation layers. dbt tests catch data contract breaks automatically.
</details>

<details>
<summary><b>Why MinIO instead of a real S3 bucket?</b></summary>

Identical S3-compatible API at zero cost. The same Spark S3A connector and boto3 code runs unchanged when deployed to AWS — no production code changes needed.
</details>

<details>
<summary><b>Why surrogate key resolution on fact load?</b></summary>

Natural keys (user email, product SKU) change over time. Surrogate integer keys resolve this and enable SCD (Slowly Changing Dimension) tracking in dbt mart models.
</details>

---

## 🗺️ Planned Enhancements

- [ ] AWS S3 as production data lake (replace MinIO for cloud deployment)
- [ ] Redshift or Snowflake as cloud warehouse
- [ ] Incremental dbt models (process only new hourly partitions)
- [ ] Data quality checks with Great Expectations
- [ ] CI/CD pipeline with GitHub Actions for dbt test automation
- [ ] Grafana dashboard wired to PostgreSQL for live pipeline monitoring
- [ ] Kafka Schema Registry with Avro for enforced event contracts

---

## 👤 Author

<table>
  <tr>
    <td align="center">
      <b>Syed Waseem</b><br/>
      AWS Certified Data Engineer Associate (DEA-C01)<br/>
      <a href="https://github.com/syedwaseem106">GitHub</a> ·
      <a href="https://linkedin.com/in/syed-waseem-i-b61132216">LinkedIn</a>
    </td>
  </tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** — contributions and pull requests are welcome.

---

<div align="center">
  <sub>Built with ❤️ using Apache Kafka · Spark · Airflow · dbt · PostgreSQL · MinIO · Docker</sub>
</div>

<!-- <div align="center">

# ⚡ Real-Time E-Commerce Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Kafka-7.5.0-231F20?style=for-the-badge&logo=apachekafka&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Spark-3.5.0-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Airflow-2.7-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/dbt_Core-1.7-FF694B?style=for-the-badge&logo=dbt&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/MinIO-S3_Compatible-C72E49?style=for-the-badge&logo=minio&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

## 📊 Dashboard Preview
Real-Time E-Commerce Analytics Live pipeline
Syed Waseem · 2026
Kafka · PySpark
<img width="716" height="577" alt="image" src="https://github.com/user-attachments/assets/01ec70ae-e9e8-4cfe-8045-ab6f7eddbd3b" />


---
## 🏗️ Pipeline Architecture
<img width="712" height="643" alt="image" src="https://github.com/user-attachments/assets/166e3e97-8d81-40d5-9203-72fc53cf378e" />


## 📊 Platform at a Glance

| Metric | Value |
|:--|:--|
| 👤 Simulated Users | 1,000 (VIP / Regular / New segments) |
| 📡 Event Types | `page_view` · `add_to_cart` · `checkout` · `purchase` · `session` |
| 🗂️ Kafka Partitions | 3 main + 1 Dead Letter Queue |
| 🗄️ Parquet Partitioning | `year / month / day / hour` |
| 🔧 dbt Models | Staging views + 4 mart models |
| 📁 BI CSV Reports | 7 Power BI / Tableau-ready exports |
| ⏰ Orchestration | Hourly 6-stage Airflow DAG |
| 🐳 Docker Services | 6 (Zookeeper, Kafka, Spark, PostgreSQL, MinIO, Airflow) |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        EVENT GENERATION LAYER                        │
│                                                                      │
│   Faker-based Behavioral Simulator                                   │
│   ├── 1,000 synthetic users with segment profiles (VIP/Regular/New) │
│   ├── Funnel-weighted event distribution                             │
│   │     page_view → add_to_cart → checkout → purchase               │
│   └── JSON event payload → Kafka Producer (Linger + GZip batch)     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    Kafka Broker (Confluent 7.5.0)
              Topic: ecommerce_events  |  3 partitions
              DLQ:   ecommerce_events_dlq  (corrupt / invalid events)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                     STREAM PROCESSING LAYER                          │
│                                                                      │
│   PySpark Structured Streaming (3.5.0)                               │
│   ├── Event-time watermarking (late arrival tolerance)               │
│   ├── Schema validation — invalid events → DLQ topic                 │
│   ├── Derived metrics:                                               │
│   │     engagement_score · funnel_stage · session_duration           │
│   └── Partitioned Parquet write → MinIO data lake                   │
│         Partition: year= / month= / day= / hour=                     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
              MinIO S3-Compatible Data Lake (raw-events/)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                      BATCH PROCESSING LAYER                          │
│                                                                      │
│   PySpark SQL + JDBC (hourly, triggered by Airflow)                  │
│   ├── dropDuplicates on event_id (idempotent re-run safe)            │
│   └── JDBC bulk load → PostgreSQL staging.stg_events                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                PostgreSQL → staging.stg_events
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    TRANSFORMATION LAYER  (dbt Core 1.7)              │
│                                                                      │
│   Staging Models              Mart Models            Seeds           │
│   ├── stg_events              ├── dim_users           ├── products   │
│   ├── stg_users               ├── dim_products        └── segments   │
│   └── stg_products            ├── dim_date                           │
│                               ├── fct_events (SCD)                   │
│                               └── agg_user_summary                   │
│                                                                      │
│   Tests: unique · not_null · accepted_values · referential integrity │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    WAREHOUSE LAYER  (Star Schema)                    │
│                                                                      │
│   dim_users ──┐                                                      │
│   dim_products┼──► fct_events ◄── dim_date                          │
│   dim_segments┘         │                                            │
│                         └──► analytics.v_reports (15 SQL queries)   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                         REPORTING LAYER                              │
│                                                                      │
│   Pandas CSV Exporter → data/exports/ → Power BI / Tableau          │
│   7 business reports: executive · daily sales · products ·           │
│   categories · user segments · conversion funnel · hourly traffic   │
└──────────────────────────────────────────────────────────────────────┘

  Orchestration: Apache Airflow 2.7 — hourly 6-stage DAG with retry handling
  Infrastructure: Docker Compose — single-command full stack deployment
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|:--|:--|:--|:--|
| **Language** | Python · SQL | 3.10 | Core pipeline scripting and analytics |
| **Message Broker** | Apache Kafka + Zookeeper | 7.5.0 | Decoupled high-velocity streaming commit log |
| **Stream Processing** | PySpark Structured Streaming | 3.5.0 | Real-time event consumption and Parquet writes |
| **Batch Processing** | PySpark SQL + JDBC | 3.5.0 | Hourly deduplication and warehouse loading |
| **Data Lake** | MinIO (S3-compatible) | Latest | Local cloud-style object storage for raw Parquet |
| **Data Warehouse** | PostgreSQL | 15 | Star schema OLAP relational storage |
| **Transformation** | dbt Core | 1.7.2 | Staging, mart models, tests, and lineage docs |
| **Orchestration** | Apache Airflow | 2.7.3 | Scheduled DAG execution, retries, monitoring |
| **Infrastructure** | Docker + Docker Compose | Latest | Fully containerized single-command deployment |

---

## ⚡ Quick Start

> **Prerequisites:** Docker Desktop · Git Bash or a Unix-compatible terminal

### 1. Clone the repository
```bash
git clone https://github.com/syedwaseem106/Real-Time-E-Commerce-Analytics-Platform.git
cd Real-Time-E-Commerce-Analytics-Platform
```

### 2. Bootstrap the full platform
```bash
./scripts/setup.sh
```
Builds all custom Docker images and spins up Zookeeper, Kafka, MinIO, Spark, PostgreSQL, and Airflow. Creates Kafka topics, initializes the database schema, and seeds 1,000 synthetic users, a 2024–2026 date spine, and the product catalog.

### 3. Run the end-to-end pipeline
```bash
./scripts/run_pipeline.sh
```
Launches Structured Streaming, generates clickstream traffic, runs Spark batch deduplication, executes dbt builds, loads surrogate fact keys into PostgreSQL, and exports all 7 BI reports to `data/exports/`.


## 📁 Project Structure

```
real-time-ecommerce-analytics/
│
├── docker-compose.yml               # Full 6-service orchestration
├── .env                             # Credentials and port configuration
├── Makefile                         # CLI shortcuts (make setup, make run, etc.)
├── requirements.txt                 # Python dependencies
│
├── scripts/
│   ├── setup.sh                     # Bootstrap all containers + seed data
│   ├── run_pipeline.sh              # End-to-end pipeline trigger
│   └── teardown.sh                  # Clean shutdown and volume reset
│
├── docker/
│   ├── spark/Dockerfile             # PySpark image with MinIO S3 connectors
│   ├── kafka/init-topics.sh         # Creates ecommerce_events + DLQ topics
│   └── postgres/init.sql            # PostgreSQL schema initialization
│
├── airflow/
│   ├── Dockerfile                   # Custom Airflow image
│   └── dags/
│       └── ecommerce_pipeline_dag.py  # 6-stage hourly orchestration DAG
│
├── src/
│   ├── event_generator/
│   │   ├── config.py                # Funnel distributions, product catalog
│   │   ├── generator.py             # Faker-based clickstream constructor
│   │   └── kafka_producer.py        # Kafka publisher with GZip batching
│   │
│   ├── spark/
│   │   ├── streaming_consumer.py    # Structured Streaming engine
│   │   ├── batch_processor.py       # Hourly deduplication Spark job
│   │   └── transformations.py       # Derived metrics, time dimensions
│   │
│   ├── warehouse/
│   │   ├── schema.sql               # PostgreSQL DDL (PKs, FKs, indexes)
│   │   ├── models.py                # SQLAlchemy ORM mappings
│   │   ├── seed_dimensions.py       # Seeds 1,000 users + date spine + products
│   │   └── load_facts.py            # Surrogate key resolution + fact load
│   │
│   ├── quality/
│   │   ├── validators.py            # Payload schema + business rule checks
│   │   └── filters.py               # Deduplication and outlier removal
│   │
│   └── analytics/
│       ├── queries.sql              # 15 advanced analytical SQL queries
│       ├── create_views.sql         # BI reporting view DDL
│       └── export_csv.py            # Pandas CSV export script
│
├── dbt_project/
│   ├── dbt_project.yml              # Materialization config
│   ├── profiles.yml                 # Dev/Prod PostgreSQL profiles
│   ├── models/
│   │   ├── staging/                 # stg_events, stg_users, stg_products
│   │   ├── marts/                   # dim_*, fct_events, agg_user_summary
│   │   └── schema.yml               # Model tests, docs, and metadata
│   ├── macros/                      # Custom Jinja macros
│   ├── tests/                       # Custom dbt data assertions
│   └── seeds/                       # Product catalog and segment CSVs
│
└── data/
    ├── sample/                      # Sample event JSON payloads
    └── exports/                     # BI-ready CSV output folder
```

---

## 🗄️ Data Model — Star Schema

### Dimension Tables

| Table | Key Columns | Description |
|:--|:--|:--|
| `dim_users` | `user_id (PK)`, `segment`, `created_at` | 1,000 synthetic users with VIP / Regular / New segments |
| `dim_products` | `product_id (PK)`, `category`, `price` | 50+ products across categories |
| `dim_date` | `date_id (PK)`, `year`, `month`, `week`, `day_of_week` | Full 2024–2026 date spine |
| `dim_segments` | `segment_id (PK)`, `segment_name`, `tier` | User tier classifications |

### Fact Table — `fct_events`

| Column | Type | Notes |
|:--|:--|:--|
| `event_id` | `VARCHAR (PK)` | Deduplicated unique event identifier |
| `user_id` | `INT (FK)` | Resolves to `dim_users` surrogate key |
| `product_id` | `INT (FK)` | Resolves to `dim_products` surrogate key |
| `date_id` | `INT (FK)` | Resolves to `dim_date` surrogate key |
| `event_type` | `VARCHAR` | `page_view` / `add_to_cart` / `checkout` / `purchase` |
| `session_id` | `VARCHAR` | Groups events into user sessions |
| `quantity` | `INT` | Units per transaction event |
| `revenue` | `DOUBLE PRECISION` | Derived: `quantity × product price` |
| `funnel_stage` | `INT` | 1–4 numeric funnel position |
| `created_at` | `TIMESTAMP` | Event timestamp with timezone |

---

## 📈 BI Report Exports
<img width="716" height="577" alt="Screenshot 2026-05-24 173836" src="https://github.com/user-attachments/assets/7a43db9f-4bfa-46f2-92ee-475d0ad37181" />


After `run_pipeline.sh` completes, Power BI / Tableau-ready CSVs land in `data/exports/`:

| Report File | Description |
|:--|:--|
| `executive_summary_report.csv` | Gross revenue, visits, transaction counts, and basket sizes |
| `daily_sales_report.csv` | Order volume, daily revenue, units sold, and day-over-day growth |
| `product_performance_report.csv` | Units sold, views, and revenue per product |
| `category_revenue_report.csv` | Revenue aggregated by product category |
| `user_segments_report.csv` | Spend metrics segmented by user tier (VIP, Regular, New) |
| `conversion_funnel_report.csv` | Drop-off rates across browse → cart → checkout → payment |
| `hourly_traffic_report.csv` | Active session volume by hour of day |

---

## 🔍 SQL Analytics — Sample Query

15 analytical queries live in `src/analytics/queries.sql`, covering funnel drop-off, revenue by segment, hourly traffic peaks, product conversion rates, repeat purchase analysis, and day-over-day growth.

```sql
-- Conversion funnel drop-off analysis
SELECT
    funnel_stage,
    event_type,
    COUNT(*)                                             AS event_count,
    ROUND(
        100.0 * COUNT(*) / FIRST_VALUE(COUNT(*)) OVER (
            ORDER BY funnel_stage
        ), 2
    )                                                    AS funnel_pct
FROM fct_events
GROUP BY funnel_stage, event_type
ORDER BY funnel_stage;
```

---

## 🔒 Data Quality & Observability

| Practice | Implementation |
|:--|:--|
| **Schema Validation** | Enforces required fields, non-null user keys, and valid quantities on every Kafka event |
| **Dead Letter Queue** | Malformed or out-of-range events route to `ecommerce_events_dlq` — main pipeline stays clean |
| **Idempotency** | Spark deduplicates on `event_id`; fact loader uses `LEFT JOIN` guard to block duplicate inserts on re-run |
| **dbt Tests** | `unique`, `not_null`, `accepted_values`, and referential integrity tests on every model build |
| **Structured Logging** | JSON logs with `pipeline_name`, `step`, `row_count`, and `duration_seconds` on every job execution |

---

## 💡 Engineering Decisions

<details>
<summary><b>Why Kafka over writing directly to the database?</b></summary>

Kafka decouples producers from consumers, absorbs traffic spikes without data loss, and enables event replay for late arrivals or pipeline failures — critical for at-least-once delivery guarantees.
</details>

<details>
<summary><b>Why Parquet partitioned by time on MinIO?</b></summary>

Columnar Parquet with `year/month/day/hour` partitioning enables partition pruning in both Spark Streaming writes and hourly batch reads, cutting scan cost as data volume grows.
</details>

<details>
<summary><b>Why dbt for transformations instead of raw SQL scripts?</b></summary>

Version-controlled, testable, self-documenting models with full lineage graphs. Staging → mart separation mirrors how professional data teams manage transformation layers. dbt tests catch data contract breaks automatically.
</details>

<details>
<summary><b>Why MinIO instead of a real S3 bucket?</b></summary>

Identical S3-compatible API at zero cost. The same Spark S3A connector and boto3 code runs unchanged when deployed to AWS — no production code changes needed.
</details>

<details>
<summary><b>Why surrogate key resolution on fact load?</b></summary>

Natural keys (user email, product SKU) change over time. Surrogate integer keys resolve this and enable SCD (Slowly Changing Dimension) tracking in dbt mart models.
</details>

---

## 🗺️ Planned Enhancements

- [ ] AWS S3 as production data lake (replace MinIO for cloud deployment)
- [ ] Redshift or Snowflake as cloud warehouse
- [ ] Incremental dbt models (process only new hourly partitions)
- [ ] Data quality checks with Great Expectations
- [ ] CI/CD pipeline with GitHub Actions for dbt test automation
- [ ] Grafana dashboard wired to PostgreSQL for live pipeline monitoring
- [ ] Kafka Schema Registry with Avro for enforced event contracts

---

## 👤 Author

<table>
  <tr>
    <td align="center">
      <b>Syed Waseem</b><br/>
      AWS Certified Data Engineer Associate (DEA-C01)<br/>
      <a href="https://github.com/syedwaseem106">GitHub</a> ·
      <a href="<a href="https://linkedin.com/in/syed-waseem-i-b61132216">LinkedIn</a>"></a>
    </td>
  </tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** — contributions and pull requests are welcome.

---

<div align="center">
  <sub>Built with ❤️ using Apache Kafka · Spark · Airflow · dbt · PostgreSQL · MinIO · Docker</sub>
</div> -->
