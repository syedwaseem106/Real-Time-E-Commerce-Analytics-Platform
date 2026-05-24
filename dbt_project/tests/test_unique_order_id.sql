-- Assert order event_ids are completely unique in fact_orders.
-- Fail test if any id is mapped multiple times.
SELECT
    event_id,
    COUNT(*) as duplicate_count
FROM {{ ref('fact_orders') }}
GROUP BY event_id
HAVING COUNT(*) > 1
