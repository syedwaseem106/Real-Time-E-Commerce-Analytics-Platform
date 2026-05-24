-- Assert purchase transactions are always positive values.
-- Fails if any order amount <= 0.00.
SELECT *
FROM {{ ref('fact_orders') }}
WHERE order_amount <= 0.00
