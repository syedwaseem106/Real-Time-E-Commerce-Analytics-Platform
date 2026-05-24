FROM apache/airflow:2.7.3-python3.10

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       git \
    && apt-get autoremove -y --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages (Providers + dbt + SQLAlchemy)
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.2.0 \
    apache-airflow-providers-postgres==5.7.1 \
    dbt-postgres==1.7.2 \
    sqlalchemy==2.0.23 \
    psycopg2-binary==2.9.9 \
    pandas==2.1.4 \
    faker==22.0.0 \
    boto3==1.34.0 \
    python-dotenv==1.0.0
