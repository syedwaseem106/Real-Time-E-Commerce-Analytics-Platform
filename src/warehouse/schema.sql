-- ==============================================================================
-- POSTGRES WAREHOUSE STAR SCHEMA DDL
-- ==============================================================================

-- Create separate target schemas to enforce data governance and architecture divisions
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;

-- ==========================================
-- 1. DIMENSION: DIM_USERS (SCD Type 1/2)
-- ==========================================
CREATE TABLE IF NOT EXISTS warehouse.dim_users (
    user_key SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    device_preference VARCHAR(30),
    segment VARCHAR(50) DEFAULT 'regular',
    first_seen_date DATE,
    last_seen_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimize filters on users
CREATE INDEX IF NOT EXISTS idx_dim_users_user_id ON warehouse.dim_users(user_id);
CREATE INDEX IF NOT EXISTS idx_dim_users_segment ON warehouse.dim_users(segment);
CREATE INDEX IF NOT EXISTS idx_dim_users_country ON warehouse.dim_users(country);

-- ==========================================
-- 2. DIMENSION: DIM_PRODUCTS
-- ==========================================
CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    base_price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimize filter and join speeds on products
CREATE INDEX IF NOT EXISTS idx_dim_products_product_id ON warehouse.dim_products(product_id);
CREATE INDEX IF NOT EXISTS idx_dim_products_category ON warehouse.dim_products(category);

-- ==========================================
-- 3. DIMENSION: DIM_TIME (Pre-populated)
-- ==========================================
CREATE TABLE IF NOT EXISTS warehouse.dim_time (
    time_key SERIAL PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT false,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER
);

-- Optimize partitioning joins
CREATE INDEX IF NOT EXISTS idx_dim_time_date ON warehouse.dim_time(full_date);
CREATE INDEX IF NOT EXISTS idx_dim_time_year_month ON warehouse.dim_time(year, month);

-- ==========================================
-- 4. FACT: FACT_EVENTS (Atomic clickstream)
-- ==========================================
CREATE TABLE IF NOT EXISTS warehouse.fact_events (
    event_key BIGSERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    user_key INTEGER REFERENCES warehouse.dim_users(user_key) ON DELETE SET NULL,
    product_key INTEGER REFERENCES warehouse.dim_products(product_key) ON DELETE SET NULL,
    time_key INTEGER REFERENCES warehouse.dim_time(time_key) ON DELETE SET NULL,
    session_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    amount DECIMAL(10,2) DEFAULT 0.00,
    quantity INTEGER DEFAULT 1,
    device VARCHAR(30),
    browser VARCHAR(30),
    event_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for rapid aggregations
CREATE INDEX IF NOT EXISTS idx_fact_events_event_type ON warehouse.fact_events(event_type);
CREATE INDEX IF NOT EXISTS idx_fact_events_timestamp ON warehouse.fact_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_fact_events_user ON warehouse.fact_events(user_key);
CREATE INDEX IF NOT EXISTS idx_fact_events_product ON warehouse.fact_events(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_events_session ON warehouse.fact_events(session_id);

-- ==========================================
-- 5. FACT: FACT_ORDERS (High-grain transactional sales)
-- ==========================================
CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_key BIGSERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    user_key INTEGER REFERENCES warehouse.dim_users(user_key) ON DELETE SET NULL,
    product_key INTEGER REFERENCES warehouse.dim_products(product_key) ON DELETE SET NULL,
    time_key INTEGER REFERENCES warehouse.dim_time(time_key) ON DELETE SET NULL,
    session_id VARCHAR(50) NOT NULL,
    order_amount DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    device VARCHAR(30),
    browser VARCHAR(30),
    order_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for reporting metrics
CREATE INDEX IF NOT EXISTS idx_fact_orders_user ON warehouse.fact_orders(user_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_product ON warehouse.fact_orders(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_timestamp ON warehouse.fact_orders(order_timestamp);

-- ==========================================
-- 6. STAGING: STG_EVENTS (Intermediate loading table)
-- ==========================================
CREATE TABLE IF NOT EXISTS staging.stg_events (
    event_id VARCHAR(50),
    user_id VARCHAR(50),
    session_id VARCHAR(50),
    event_type VARCHAR(30),
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    amount DECIMAL(10,2),
    quantity INTEGER,
    device VARCHAR(30),
    browser VARCHAR(30),
    city VARCHAR(100),
    country VARCHAR(100),
    event_timestamp TIMESTAMP,
    event_date DATE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
