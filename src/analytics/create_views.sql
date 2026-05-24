-- ==============================================================================
-- BI-READY REPORTING VIEWS FOR DASHBOARDS
-- ==============================================================================

-- Create target schema if missing
CREATE SCHEMA IF NOT EXISTS analytics;

-- 1. Daily Sales Summary View
CREATE OR REPLACE VIEW analytics.v_daily_sales_summary AS
SELECT 
    t.full_date AS order_date,
    t.year,
    t.month_name AS month,
    t.day_name AS day_of_week,
    t.is_weekend,
    COUNT(f.order_key) AS total_orders,
    SUM(f.order_amount) AS total_revenue,
    SUM(f.quantity) AS total_units_sold,
    COUNT(DISTINCT f.user_key) AS unique_customers,
    ROUND(SUM(f.order_amount) / NULLIF(COUNT(f.order_key), 0), 2) AS average_order_value
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_time t ON f.time_key = t.time_key
GROUP BY t.full_date, t.year, t.month_name, t.day_name, t.is_weekend;

-- 2. Product Performance View
CREATE OR REPLACE VIEW analytics.v_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.brand,
    p.base_price,
    COUNT(f.order_key) AS times_ordered,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.order_amount) AS generated_revenue
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category, p.subcategory, p.brand, p.base_price;

-- 3. Category Revenue View
CREATE OR REPLACE VIEW analytics.v_category_revenue AS
SELECT 
    p.category,
    COUNT(DISTINCT f.order_key) AS order_count,
    SUM(f.quantity) AS units_sold,
    SUM(f.order_amount) AS total_revenue
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
GROUP BY p.category;

-- 4. User Segments View
CREATE OR REPLACE VIEW analytics.v_user_segments AS
SELECT 
    segment,
    COUNT(user_key) AS user_count,
    ROUND(AVG(total_orders), 2) AS average_orders_per_customer,
    SUM(total_spend) AS total_spent,
    ROUND(AVG(total_spend), 2) AS average_lifetime_value
FROM warehouse.dim_users -- Safely references dim_users (materialized by dbt or seeded)
GROUP BY segment;

-- 5. Conversion Funnel View
CREATE OR REPLACE VIEW analytics.v_conversion_funnel AS
WITH session_stages AS (
    SELECT 
        session_id,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) AS stage_home,
        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS stage_view,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS stage_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS stage_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS stage_purchase
    FROM warehouse.fact_events
    GROUP BY session_id
)
SELECT
    COUNT(session_id) AS total_sessions,
    SUM(stage_home) AS home_visits,
    SUM(stage_view) AS product_views,
    SUM(stage_cart) AS cart_additions,
    SUM(stage_checkout) AS checkout_initiations,
    SUM(stage_purchase) AS purchases
FROM session_stages;

-- 6. Hourly Web Traffic View
CREATE OR REPLACE VIEW analytics.v_hourly_traffic AS
SELECT 
    EXTRACT(HOUR FROM event_timestamp) AS active_hour,
    COUNT(event_id) AS total_clicks,
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS total_purchases
FROM warehouse.fact_events
GROUP BY active_hour;

-- 7. Executive Dashboard Summary View
CREATE OR REPLACE VIEW analytics.v_executive_summary AS
SELECT 
    (SELECT SUM(order_amount) FROM warehouse.fact_orders) AS lifetime_gross_revenue,
    (SELECT COUNT(*) FROM warehouse.fact_orders) AS total_transactions,
    (SELECT COUNT(DISTINCT user_key) FROM warehouse.dim_users) AS total_registered_users,
    (SELECT COUNT(DISTINCT session_id) FROM warehouse.fact_events) AS total_visits,
    ROUND((SELECT SUM(order_amount) FROM warehouse.fact_orders) / (SELECT COUNT(*) FROM warehouse.fact_orders), 2) AS average_basket_value;
