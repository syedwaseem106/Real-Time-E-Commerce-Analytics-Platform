WITH source AS (
    SELECT * FROM {{ source('raw', 'stg_events') }}
),

renamed AS (
    SELECT
        CAST(event_id AS VARCHAR(50)) AS event_id,
        CAST(user_id AS VARCHAR(50)) AS user_id,
        CAST(session_id AS VARCHAR(50)) AS session_id,
        LOWER(TRIM(CAST(event_type AS VARCHAR(30)))) AS event_type,
        CAST(product_id AS VARCHAR(50)) AS product_id,
        INITCAP(TRIM(CAST(product_name AS VARCHAR(200)))) AS product_name,
        INITCAP(TRIM(CAST(category AS VARCHAR(100)))) AS category,
        COALESCE(CAST(amount AS DECIMAL(10,2)), 0.00) AS amount,
        COALESCE(CAST(quantity AS INTEGER), 1) AS quantity,
        LOWER(CAST(device AS VARCHAR(30))) AS device,
        LOWER(CAST(browser AS VARCHAR(30))) AS browser,
        CAST(city AS VARCHAR(100)) AS city,
        CAST(country AS VARCHAR(100)) AS country,
        CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
        CAST(event_date AS DATE) AS event_date,
        CAST(loaded_at AS TIMESTAMP) AS loaded_at
    FROM source
    WHERE event_id IS NOT NULL
      AND user_id IS NOT NULL
      AND session_id IS NOT NULL
)

SELECT * FROM renamed
