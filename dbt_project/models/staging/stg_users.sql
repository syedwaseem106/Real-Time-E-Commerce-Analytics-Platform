WITH raw_events AS (
    SELECT * FROM {{ source('raw', 'stg_events') }}
),

user_activities AS (
    SELECT
        user_id,
        username,
        email,
        city,
        country,
        device AS device_preference,
        event_date,
        event_timestamp,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_timestamp DESC) as row_num
    FROM raw_events
    WHERE user_id IS NOT NULL
)

SELECT
    CAST(user_id AS VARCHAR(50)) AS user_id,
    COALESCE(CAST(username AS VARCHAR(100)), 'Anonymous') AS username,
    COALESCE(CAST(email AS VARCHAR(150)), 'anonymous@example.com') AS email,
    CAST(city AS VARCHAR(100)) AS city,
    CAST(country AS VARCHAR(100)) AS country,
    CAST(device_preference AS VARCHAR(30)) AS device_preference,
    CAST(event_date AS DATE) AS last_active_date
FROM user_activities
WHERE row_num = 1
