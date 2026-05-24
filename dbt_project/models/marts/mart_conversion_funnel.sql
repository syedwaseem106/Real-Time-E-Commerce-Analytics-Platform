WITH stg_events AS (
    SELECT * FROM {{ ref('stg_events') }}
),

session_activity AS (
    SELECT
        event_date,
        session_id,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) AS visited_home,
        MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS initiated_checkout,
        MAX(CASE WHEN event_type IN ('purchase', 'payment') THEN 1 ELSE 0 END) AS completed_purchase
    FROM stg_events
    GROUP BY event_date, session_id
),

daily_funnel AS (
    SELECT
        event_date,
        COUNT(DISTINCT session_id) AS total_sessions,
        SUM(visited_home) AS home_visits,
        SUM(viewed_product) AS product_views,
        SUM(added_to_cart) AS cart_additions,
        SUM(initiated_checkout) AS checkout_initiations,
        SUM(completed_purchase) AS purchases
    FROM session_activity
    GROUP BY event_date
)

SELECT
    event_date,
    total_sessions,
    home_visits,
    product_views,
    cart_additions,
    checkout_initiations,
    purchases,
    
    # Session conversion ratios
    CASE WHEN total_sessions = 0 THEN 0.00 ELSE ROUND((product_views::DECIMAL / total_sessions) * 100.00, 2) END AS view_drop_pct,
    CASE WHEN product_views = 0 THEN 0.00 ELSE ROUND((cart_additions::DECIMAL / product_views) * 100.00, 2) END AS cart_drop_pct,
    CASE WHEN cart_additions = 0 THEN 0.00 ELSE ROUND((checkout_initiations::DECIMAL / cart_additions) * 100.00, 2) END AS checkout_drop_pct,
    CASE WHEN checkout_initiations = 0 THEN 0.00 ELSE ROUND((purchases::DECIMAL / checkout_initiations) * 100.00, 2) END AS purchase_drop_pct,
    
    # Net overall conversion rate
    CASE WHEN total_sessions = 0 THEN 0.00 ELSE ROUND((purchases::DECIMAL / total_sessions) * 100.00, 2) END AS net_conversion_rate_pct,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM daily_funnel
