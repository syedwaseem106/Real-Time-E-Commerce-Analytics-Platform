-- Assert user_id is never null inside final fact tables.
-- Fails if any order record has a blank user.
SELECT *
FROM {{ ref('fact_orders') }}
WHERE user_id IS NULL
