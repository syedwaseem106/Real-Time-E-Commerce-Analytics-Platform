WITH stg_events AS (
    SELECT * FROM {{ ref('stg_events') }}
),

dim_users AS (
    SELECT * FROM {{ ref('dim_users') }}
),

dim_products AS (
    SELECT * FROM {{ ref('dim_products') }}
)

SELECT
    e.event_id AS order_id,
    e.event_id,
    u.user_id,
    p.product_id,
    e.session_id,
    e.amount AS order_amount,
    e.quantity,
    e.device,
    e.browser,
    e.city,
    e.country,
    e.event_timestamp AS order_timestamp,
    e.event_date AS order_date,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM stg_events e
INNER JOIN dim_users u ON e.user_id = u.user_id
INNER JOIN dim_products p ON e.product_id = p.product_id
WHERE e.event_type IN ('purchase', 'payment')
