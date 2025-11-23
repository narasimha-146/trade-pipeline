/*
Query 1: Calculates yearly totals for shipments, including total value, duty paid, and grand total.
Query 2: Computes Year-over-Year (YoY) growth for total value by comparing each year's total with the previous year's.
*/

-- Query 1: Yearly Totals
SELECT
    EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))::INT AS year,
    SUM("TOTAL VALUE_INR") AS total_value,
    SUM("DUTY PAID_INR") AS duty_paid,
    SUM("Grand Total (INR)") AS grand_total
FROM shipments
GROUP BY year
ORDER BY year;

-- Query 2: Year-over-Year Growth
WITH yearly_totals AS (
    SELECT
        EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))::INT AS year,
        SUM("TOTAL VALUE_INR") AS total_value
    FROM shipments
    GROUP BY year
)
SELECT
    year,
    total_value,
    LAG(total_value) OVER (ORDER BY year) AS prev_total_value,
    CASE 
        WHEN LAG(total_value) OVER (ORDER BY year) IS NULL THEN NULL
        ELSE ((total_value - LAG(total_value) OVER (ORDER BY year)) / LAG(total_value) OVER (ORDER BY year)) * 100
    END AS yoy_growth_total_value
FROM yearly_totals
ORDER BY year;
