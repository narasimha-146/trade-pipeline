/*
This query performs a Pareto analysis on HSN codes:
1. Computes total trade value per HSN code.
2. Ranks HSN codes by value and calculates cumulative totals.
3. Groups top 25 codes individually, all others into 'Others'.
4. Calculates % contribution of each group to total trade value.
*/


WITH supplier_years AS (
    SELECT
        "IEC",
        MIN(EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))) AS first_year,  -- first shipment year
        MAX(EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))) AS last_year    -- last shipment year
    FROM shipments
    GROUP BY "IEC"
),
supplier_status AS (
    SELECT
        "IEC",
        first_year,
        last_year,
        CASE 
            WHEN last_year = 2025 THEN 'Active'
            ELSE 'Churned'
        END AS status
    FROM supplier_years
)
SELECT *
FROM supplier_status
ORDER BY status DESC, "IEC";
