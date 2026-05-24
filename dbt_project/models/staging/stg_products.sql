WITH raw_events AS (
    SELECT * FROM {{ source('raw', 'stg_events') }}
),

product_details AS (
    SELECT
        product_id,
        product_name,
        category,
        amount AS price,
        ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY event_timestamp DESC) as row_num
    FROM raw_events
    WHERE product_id IS NOT NULL
)

SELECT
    CAST(product_id AS VARCHAR(50)) AS product_id,
    COALESCE(CAST(product_name AS VARCHAR(200)), 'Unknown Product') AS product_name,
    COALESCE(CAST(category AS VARCHAR(100)), 'Unknown Category') AS category,
    COALESCE(CAST(price AS DECIMAL(10,2)), 0.00) AS base_price
FROM product_details
WHERE row_num = 1
