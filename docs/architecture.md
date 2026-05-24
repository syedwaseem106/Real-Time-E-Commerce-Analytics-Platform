# System Architecture & Design Deep-Dive

This document provides a detailed breakdown of the architectural design, network topology, storage tiers, and data schemas deployed inside our E-Commerce Data Engineering Platform.

---

## 📊 End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Clickstream Ingestion
        Gen["Faker Event Generator\n(Python)"] -->|JSON Payloads| Prod["Kafka Producer\n(Retries & Compression)"]
        Prod -->|Topic: ecommerce_events| Broker["Kafka Broker\n(3 Partitions)"]
    end

    subgraph Data Lake & Streaming
        Broker -->|Subscribe| SparkStream["Spark Structured Streaming\n(Watermarking & Filter)"]
        SparkStream -->|Partitioned Parquet| MinIO["MinIO Object Storage\n(raw-events bucket)"]
    end

    subgraph Orchestration & Modeling
        MinIO -->|Scheduled Read| SparkBatch["Spark Batch Processor\n(Deduplication)"]
        SparkBatch -->|JDBC Append| PGStage["PostgreSQL Staging\n(staging.stg_events)"]
        
        Airflow["Apache Airflow\n(LocalExecutor)"] -.->|Orchestrates| SparkBatch
        Airflow -.->|Orchestrates| DBT["dbt Core\n(staging & marts)"]
        Airflow -.->|Orchestrates| PGWH["PostgreSQL Fact Load"]
        
        DBT -->|Materialize views/tables| PGStage
        PGStage -->|Join dimensions| PGWH["PostgreSQL Warehouse\n(Star Schema facts)"]
    end

    subgraph Analytics Layer
        PGWH -->|Aggregate Views| Views["analytics.v_reports"]
        Views -->|Python Export| CSV["data/exports/*.csv"]
        CSV -->|Downstream BI| BI["Power BI / Tableau"]
    end

    classDef ing fill:#f9f,stroke:#333,stroke-width:2px;
    classDef stream fill:#bbf,stroke:#333,stroke-width:2px;
    classDef wh fill:#f96,stroke:#333,stroke-width:2px;
    classDef bi fill:#bfb,stroke:#333,stroke-width:2px;
    
    class Gen,Prod,Broker ing;
    class SparkStream,MinIO stream;
    class SparkBatch,PGStage,DBT,PGWH,Airflow wh;
    class Views,CSV,BI bi;
```

---

## 🛣️ Data Flow Lanes

### ⚡ The Real-Time Streaming Lane
1. **Source Generation:** A stateful Python Faker script runs. It maintains user cookie states, generating multi-step session sequences (e.g. searching products, adding to cart, completing checkouts).
2. **Buffer Ingestion:** The `EcommerceKafkaProducer` writes JSON arrays of click events into our Kafka topic `ecommerce_events`. It is configured with `acks=all` (ensuring at least one broker commits the event), `linger_ms=10` (buffering for network throughput), and `compression_type=gzip` (reducing bandwidth).
3. **Stream Parsing:** `streaming_consumer.py` subscribes to Kafka using PySpark. It maps the raw string column into a strict StructType schema, filters blank or negative values, adds a **10-minute watermark** to manage late-arriving packets, and appends the records to S3 raw-events.
4. **Lake Partitioning:** Spark writes Parquet files divided into sub-directories like `event_date=YYYY-MM-DD/`, isolating daily records and optimizing downstream column scans.

### ⚙️ The Scheduled Batch Lane
1. **Airflow Orchestration:** Every hour, Apache Airflow executes the `ecommerce_analytics_pipeline` DAG. 
2. **Batch Deduplication:** Airflow runs the Spark Batch Processor, which loads the latest date partition from MinIO, filters any duplicates via `dropDuplicates(['event_id'])`, and loads the records into PostgreSQL `staging.stg_events`.
3. **dbt Modeling:** Airflow triggers dbt to parse staged click records. dbt compiles models that separate raw attributes into staging views (`stg_events`, `stg_users`, `stg_products`) and computes lifetime totals to build dimension tables (`dim_users`, `dim_products`).
4. **Surrogate Key Loading:** Airflow runs `load_facts.py` which executes PostgreSQL insert transactions. It resolves late-arriving dimensions and joins staging fields against `dim_users`, `dim_products`, and `dim_time` to load surrogate keys into `fact_events` and `fact_orders`.
5. **Dashboard Updates:** Finally, Airflow executes views updates and CSV exports to prepare data reports for BI dashboards.

---

## 🗄️ Relational Database Schema Model (Star Schema)

Our data warehouse uses a Kimball Star Schema model optimized for Analytical queries (OLAP):

```mermaid
erDiagram
    dim_users {
        int user_key PK
        varchar user_id UK
        varchar username
        varchar email
        varchar city
        varchar country
        varchar segment
        date first_seen_date
        date last_seen_date
    }
    dim_products {
        int product_key PK
        varchar product_id UK
        varchar product_name
        varchar category
        varchar subcategory
        varchar brand
        decimal base_price
    }
    dim_time {
        int time_key PK
        date full_date UK
        int year
        int quarter
        int month
        varchar month_name
        int week_of_year
        int day_of_month
        int day_of_week
        varchar day_name
        boolean is_weekend
    }
    fact_orders {
        bigint order_key PK
        varchar event_id UK
        int user_key FK
        int product_key FK
        int time_key FK
        varchar session_id
        decimal order_amount
        int quantity
        varchar device
        varchar browser
        timestamp order_timestamp
    }
    fact_events {
        bigint event_key PK
        varchar event_id UK
        int user_key FK
        int product_key FK
        int time_key FK
        varchar session_id
        varchar event_type
        decimal amount
        int quantity
        varchar device
        varchar browser
        timestamp event_timestamp
    }

    dim_users ||--o{ fact_orders : purchases
    dim_products ||--o{ fact_orders : contains
    dim_time ||--o{ fact_orders : placed_on

    dim_users ||--o{ fact_events : generates
    dim_products ||--o{ fact_events : targeted_by
    dim_time ||--o{ fact_events : occurs_on
```

---

## 🔒 Security & Network Isolation

All platform containers reside on a shared bridge network: `ecommerce-network`. 
* **Port Protection:** Inside this network, services resolve to internal container hostnames (e.g. `postgres:5432`, `kafka:29092`, `spark-master:7077`). Only necessary operational endpoints are mapped externally to localhost (e.g. Postgres port `5432`, Kafka port `9092`, Airflow port `8081`), ensuring full database isolation.
* **Volume Persistence:** Container states are mapped onto named docker volumes (`postgres_data`, `minio_data`, etc.), meaning database assets persist even when containers are restarted.
