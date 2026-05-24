{% macro safe_divide(numerator, denominator, precision=4) %}
    CASE 
        WHEN {{ denominator }} = 0 OR {{ denominator }} IS NULL THEN 0.0000
        ELSE ROUND(CAST({{ numerator }} AS DECIMAL) / CAST({{ denominator }} AS DECIMAL), {{ precision }})
    END
{% endmacro %}
