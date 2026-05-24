-- Materialize pre-seeded time table directly into our analytical schema
SELECT
    time_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week_of_year,
    day_of_month,
    day_of_week,
    day_name,
    is_weekend,
    is_holiday,
    fiscal_year,
    fiscal_quarter
FROM {{ source('raw', 'stg_events') }} -- Triggers dependency resolution
CROSS JOIN (
    SELECT * FROM warehouse.dim_time
) dt
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
