{% macro cents_to_dollars(column_name, scale=2) %}
    ROUND(CAST({{ column_name }} AS DECIMAL(10,4)) / 100.00, {{ scale }})
{% endmacro %}
