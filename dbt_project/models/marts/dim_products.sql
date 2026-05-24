WITH stg_products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

stg_events AS (
    SELECT * FROM {{ ref('stg_events') }}
),

product_performance AS (
    SELECT
        product_id,
        COUNT(CASE WHEN event_type = 'product_view' THEN 1 END) AS total_views,
        COUNT(CASE WHEN event_type = 'add_to_cart' THEN 1 END) AS total_cart_additions,
        SUM(CASE WHEN event_type IN ('purchase', 'payment') THEN quantity ELSE 0 END) AS units_sold,
        SUM(CASE WHEN event_type IN ('purchase', 'payment') THEN amount ELSE 0.00 END) AS total_revenue
    FROM stg_events
    GROUP BY product_id
)

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.base_price,
    COALESCE(perf.total_views, 0) AS total_views,
    COALESCE(perf.total_cart_additions, 0) AS total_cart_additions,
    COALESCE(perf.units_sold, 0) AS units_sold,
    COALESCE(perf.total_revenue, 0.00) AS total_revenue,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM stg_products p
LEFT JOIN product_performance perf ON p.product_id = perf.product_id
