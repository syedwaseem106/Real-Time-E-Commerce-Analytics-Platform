-- Assert only allowed click actions populate the pipeline staging model.
-- Fails if any event has an un-cataloged event_type.
SELECT *
FROM {{ ref('stg_events') }}
WHERE event_type NOT IN ('page_view', 'product_view', 'add_to_cart', 'remove_from_cart', 'checkout', 'purchase', 'payment')
