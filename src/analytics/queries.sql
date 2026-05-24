-- ==============================================================================
-- PRODUCTION E-COMMERCE ANALYTICAL QUERY PORTFOLIO
-- ==============================================================================

-- 1. Top 20 Selling Products by Revenue
-- Calculates cumulative sales volume and revenue generated per product
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(f.order_key) AS total_orders,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.order_amount) AS total_revenue
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 20;

-- 2. Revenue and Growth by Category
-- Computes the total sales breakdown and relative contribution of each category
WITH total_sales AS (
    SELECT SUM(order_amount) AS grand_total FROM warehouse.fact_orders
)
SELECT 
    p.category,
    COUNT(f.order_key) AS total_transactions,
    SUM(f.order_amount) AS category_revenue,
    ROUND((SUM(f.order_amount) / (SELECT grand_total FROM total_sales)) * 100.00, 2) AS contribution_percentage
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 3. Daily Active Users (DAU) & Engagement Density
-- Establishes the daily volume of unique customers active in our storefront
SELECT 
    t.full_date,
    COUNT(DISTINCT f.user_key) AS daily_active_users,
    COUNT(f.event_key) AS total_actions,
    ROUND(COUNT(f.event_key)::DECIMAL / COUNT(DISTINCT f.user_key), 2) AS actions_per_user
FROM warehouse.fact_events f
INNER JOIN warehouse.dim_time t ON f.time_key = t.time_key
GROUP BY t.full_date
ORDER BY t.full_date DESC
LIMIT 30;

-- 4. Conversion Funnel Drop-off Analysis
-- Tracks checkout drop-offs across session stages: view -> cart -> checkout -> buy
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
    SUM(stage_purchase) AS purchases,
    
    -- Stage conversion percentages
    ROUND((SUM(stage_view)::DECIMAL / COUNT(session_id)) * 100.00, 2) AS home_to_view_pct,
    ROUND((SUM(stage_cart)::DECIMAL / NULLIF(SUM(stage_view), 0)) * 100.00, 2) AS view_to_cart_pct,
    ROUND((SUM(stage_checkout)::DECIMAL / NULLIF(SUM(stage_cart), 0)) * 100.00, 2) AS cart_to_checkout_pct,
    ROUND((SUM(stage_purchase)::DECIMAL / NULLIF(SUM(stage_checkout), 0)) * 100.00, 2) AS checkout_to_purchase_pct,
    ROUND((SUM(stage_purchase)::DECIMAL / COUNT(session_id)) * 100.00, 2) AS total_sessions_conversion_pct
FROM session_stages;

-- 5. Customer Retention Cohorts (Month-over-Month)
-- Analyzes transaction retention across monthly customer cohorts
WITH user_signup AS (
    SELECT 
        user_key,
        DATE_TRUNC('month', first_seen_date) AS cohort_month
    FROM warehouse.dim_users
),
user_orders AS (
    SELECT DISTINCT
        user_key,
        DATE_TRUNC('month', order_timestamp) AS order_month
    FROM warehouse.fact_orders
)
SELECT 
    s.cohort_month,
    o.order_month,
    -- Retention age in months
    EXTRACT(YEAR FROM o.order_month) * 12 + EXTRACT(MONTH FROM o.order_month) - 
    (EXTRACT(YEAR FROM s.cohort_month) * 12 + EXTRACT(MONTH FROM s.cohort_month)) AS period,
    COUNT(DISTINCT o.user_key) AS active_users
FROM user_signup s
INNER JOIN user_orders o ON s.user_key = o.user_key
GROUP BY s.cohort_month, o.order_month
ORDER BY cohort_month, order_month;

-- 6. Moving 7-Day Average Sales Trends
-- Employs SQL window functions to smooth seasonal spikes and reveal net growth trends
WITH daily_revenue AS (
    SELECT 
        t.full_date,
        SUM(f.order_amount) AS revenue
    FROM warehouse.fact_orders f
    INNER JOIN warehouse.dim_time t ON f.time_key = t.time_key
    GROUP BY t.full_date
)
SELECT 
    full_date,
    revenue,
    ROUND(AVG(revenue) OVER (
        ORDER BY full_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_7day_avg_revenue
FROM daily_revenue
ORDER BY full_date DESC;

-- 7. High-Volume Transaction Hours (Peak Performance Analysis)
-- Groups order volume by hour of the day to optimize server workloads and advertising spend
SELECT 
    EXTRACT(HOUR FROM order_timestamp) AS order_hour,
    COUNT(order_key) AS total_orders,
    SUM(order_amount) AS total_sales,
    ROUND(AVG(order_amount), 2) AS average_order_value
FROM warehouse.fact_orders
GROUP BY order_hour
ORDER BY total_sales DESC;

-- 8. Device Preference and Funnel Rates
-- Compares customer behavior and checkout metrics between Mobile, Desktop, and Tablet clients
SELECT 
    device,
    COUNT(order_key) AS total_orders,
    SUM(order_amount) AS total_sales,
    ROUND(AVG(order_amount), 2) AS average_order_value,
    SUM(quantity) AS units_sold
FROM warehouse.fact_orders
GROUP BY device
ORDER BY total_sales DESC;

-- 9. Rolling Average Order Value (AOV)
-- Computes the Average Order Value trended across transaction days
SELECT 
    t.full_date,
    COUNT(f.order_key) AS transactions,
    SUM(f.order_amount) AS sales,
    ROUND(SUM(f.order_amount) / COUNT(f.order_key), 2) AS average_order_value
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_time t ON f.time_key = t.time_key
GROUP BY t.full_date
ORDER BY t.full_date DESC
LIMIT 30;

-- 10. Top 15 Customer LTV (Lifetime Value)
-- Identifies our highest-value clients based on total accumulated order values
SELECT 
    u.user_id,
    u.username,
    u.city,
    u.country,
    u.segment,
    COUNT(f.order_key) AS order_count,
    SUM(f.order_amount) AS lifetime_spend
FROM warehouse.fact_orders f
INNER JOIN warehouse.dim_users u ON f.user_key = u.user_key
GROUP BY u.user_id, u.username, u.city, u.country, u.segment
ORDER BY lifetime_spend DESC
LIMIT 15;

-- 11. Cart Abandonment Rate by Product Category
-- Computes the percentage of cart additions that fail to convert to completed purchases
WITH cart_adds AS (
    SELECT 
        p.category,
        COUNT(f.event_key) AS additions
    FROM warehouse.fact_events f
    INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
    WHERE f.event_type = 'add_to_cart'
    GROUP BY p.category
),
purchases AS (
    SELECT 
        p.category,
        COUNT(f.order_key) AS conversions
    FROM warehouse.fact_orders f
    INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
    GROUP BY p.category
)
SELECT 
    c.category,
    c.additions AS total_cart_additions,
    COALESCE(p.conversions, 0) AS total_purchases,
    ROUND(((c.additions - COALESCE(p.conversions, 0))::DECIMAL / c.additions) * 100.00, 2) AS abandonment_rate_pct
FROM cart_adds c
LEFT JOIN purchases p ON c.category = p.category
ORDER BY abandonment_rate_pct DESC;

-- 12. Session Engagement and Lifespans
-- Analyzes session durations and average interactions per visit
WITH session_times AS (
    SELECT 
        session_id,
        MIN(event_timestamp) AS start_time,
        MAX(event_timestamp) AS end_time,
        COUNT(event_id) AS total_clicks
    FROM warehouse.fact_events
    GROUP BY session_id
)
SELECT 
    AVG(end_time - start_time) AS average_session_duration,
    AVG(total_clicks) AS average_clicks_per_session,
    MAX(total_clicks) AS max_clicks_in_a_session
FROM session_times;

-- 13. New vs Returning Customer Sales Breakdown
-- Tracks spending balances between fresh signups and loyal repeat customers
WITH customer_orders AS (
    SELECT 
        f.user_key,
        f.order_amount,
        f.order_timestamp,
        ROW_NUMBER() OVER (PARTITION BY f.user_key ORDER BY f.order_timestamp ASC) as order_index
    FROM warehouse.fact_orders f
)
SELECT 
    CASE WHEN order_index = 1 THEN 'New Customer' ELSE 'Returning Customer' END AS customer_type,
    COUNT(*) AS total_orders,
    SUM(order_amount) AS total_revenue,
    ROUND(AVG(order_amount), 2) AS average_order_value
FROM customer_orders
GROUP BY customer_type;

-- 14. Week-over-Week Sales Growth
-- Tracks changes in transactional performance compared to prior calendar weeks
WITH weekly_revenue AS (
    SELECT 
        t.year,
        t.week_of_year,
        SUM(f.order_amount) AS weekly_sales
    FROM warehouse.fact_orders f
    INNER JOIN warehouse.dim_time t ON f.time_key = t.time_key
    GROUP BY t.year, t.week_of_year
),
weekly_growth AS (
    SELECT 
        year,
        week_of_year,
        weekly_sales,
        LAG(weekly_sales) OVER (ORDER BY year, week_of_year) AS prior_week_sales
    FROM weekly_revenue
)
SELECT 
    year,
    week_of_year,
    weekly_sales,
    COALESCE(prior_week_sales, 0.00) AS prior_week_sales,
    CASE 
        WHEN prior_week_sales IS NULL OR prior_week_sales = 0 THEN 0.00
        ELSE ROUND(((weekly_sales - prior_week_sales) / prior_week_sales) * 100.00, 2)
    END AS wow_growth_pct
FROM weekly_growth
ORDER BY year DESC, week_of_year DESC
LIMIT 12;

-- 15. Cross-Category Purchase Correlations
-- Reveals market basket patterns to determine which categories are frequently purchased together
WITH customer_purchases AS (
    SELECT DISTINCT
        session_id,
        p.category
    FROM warehouse.fact_orders f
    INNER JOIN warehouse.dim_products p ON f.product_key = p.product_key
)
SELECT 
    cp1.category AS category_a,
    cp2.category AS category_b,
    COUNT(*) AS joint_purchases
FROM customer_purchases cp1
INNER JOIN customer_purchases cp2 ON cp1.session_id = cp2.session_id AND cp1.category < cp2.category
GROUP BY cp1.category, cp2.category
ORDER BY joint_purchases DESC
LIMIT 15;
