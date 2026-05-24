WITH stg_users AS (
    SELECT * FROM {{ ref('stg_users') }}
),

stg_events AS (
    SELECT * FROM {{ ref('stg_events') }}
),

user_spend AS (
    SELECT
        user_id,
        MIN(event_date) AS first_seen_date,
        MAX(event_date) AS last_seen_date,
        COUNT(DISTINCT CASE WHEN event_type IN ('purchase', 'payment') THEN event_id END) AS total_orders,
        SUM(CASE WHEN event_type IN ('purchase', 'payment') THEN amount ELSE 0.00 END) AS total_spend,
        COUNT(DISTINCT session_id) AS total_sessions
    FROM stg_events
    GROUP BY user_id
)

SELECT
    u.user_id,
    u.username,
    u.email,
    u.city,
    u.country,
    u.device_preference,
    COALESCE(s.total_orders, 0) AS total_orders,
    COALESCE(s.total_spend, 0.00) AS total_spend,
    COALESCE(s.total_sessions, 0) AS total_sessions,
    s.first_seen_date,
    s.last_seen_date,
    
    # Custom business rules segments
    CASE
        WHEN s.total_spend >= 500.00 THEN 'VIP'
        WHEN s.total_spend >= 100.00 AND s.total_spend < 500.00 THEN 'Frequent Buyer'
        WHEN s.total_spend > 0.00 AND s.total_spend < 100.00 THEN 'Bargain Hunter'
        ELSE 'Regular'
    END AS segment,
    
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM stg_users u
LEFT JOIN user_spend s ON u.user_id = s.user_id
