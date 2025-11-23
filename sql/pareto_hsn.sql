/*
This query performs a Pareto analysis on HSN codes:
1. Computes total trade value per HSN code.
2. Ranks HSN codes by value and calculates cumulative totals.
3. Groups top 25 codes individually, all others into 'Others'.
4. Calculates % contribution of each group to total trade value.
*/

WITH hsn_totals AS (
    SELECT
        "HS CODE",
        SUM("TOTAL VALUE_INR") AS hsn_value
    FROM shipments
    GROUP BY "HS CODE"
),
hsn_ranked AS (
    SELECT
        "HS CODE",
        hsn_value,
        SUM(hsn_value) OVER (ORDER BY hsn_value DESC) AS cumulative_value,
        SUM(hsn_value) OVER () AS total_value,
        ROW_NUMBER() OVER (ORDER BY hsn_value DESC) AS rank
    FROM hsn_totals
)
SELECT
    CASE 
        WHEN rank <= 25 THEN "HS CODE"::TEXT
        ELSE 'Others'
    END AS hsn_code,
    SUM(hsn_value) AS hsn_value,
    ROUND((SUM(hsn_value) * 100.0 / MAX(total_value))::numeric, 2) AS pct_contribution
FROM hsn_ranked
GROUP BY CASE WHEN rank <= 25 THEN "HS CODE"::TEXT ELSE 'Others' END
ORDER BY hsn_value DESC;
