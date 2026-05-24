WITH fact_orders AS (
    SELECT * FROM {{ ref('fact_orders') }}
),

daily_aggregations AS (
    SELECT
        order_date,
        COUNT(DISTINCT event_id) AS total_orders,
        SUM(order_amount) AS total_revenue,
        SUM(quantity) AS total_units_sold,
        COUNT(DISTINCT user_id) AS unique_customers,
        AVG(order_amount) AS avg_order_value
    FROM fact_orders
    GROUP BY order_date
),

daily_trends AS (
    SELECT
        order_date,
        total_orders,
        total_revenue,
        total_units_sold,
        unique_customers,
        avg_order_value,
        # Fetch previous day metrics using window lag functions
        LAG(total_revenue) OVER (ORDER BY order_date) AS prev_day_revenue,
        SUM(total_revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
    FROM daily_aggregations
)

SELECT
    order_date,
    total_orders,
    total_revenue,
    total_units_sold,
    unique_customers,
    avg_order_value,
    COALESCE(prev_day_revenue, 0.00) AS prev_day_revenue,
    
    # Calculate Day-over-Day Revenue Growth
    CASE
        WHEN prev_day_revenue IS NULL OR prev_day_revenue = 0 THEN 0.00
        ELSE ROUND(((total_revenue - prev_day_revenue) / prev_day_revenue) * 100.00, 2)
    END AS dod_revenue_growth_pct,
    
    cumulative_revenue,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM daily_trends
