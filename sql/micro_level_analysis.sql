/*
Phase 5: Micro-Level & Unit Economics Analysis

This SQL file performs detailed analyses on the shipments data:

1. Model-Level Insights:
   - Summarizes total quantity, average, and median unit price per model and year.

2. Supplier Comparison:
   - Compares average unit prices for the same model across different suppliers per year.

3. Capacity Analysis:
   - Aggregates total quantities per capacity to identify the highest-volume sizes.

4. Duty & Cost Anomalies:
   - Calculates duty percentage and flags rows where the duty is > 2 standard deviations from the mean.
*/


-- Model-level summary with year extracted
SELECT 
    "Model Name" AS model_name,
    "Model Number" AS model_number,
    EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))::INT AS year,
    SUM("Qty") AS total_quantity,
    AVG("UNIT PRICE_INR") AS avg_unit_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "UNIT PRICE_INR") AS median_unit_price
FROM shipments
GROUP BY "Model Name", "Model Number", year
ORDER BY total_quantity DESC;

-- Compare unit price per model across suppliers
SELECT
    "Model Name" AS model_name,
    "Model Number" AS model_number,
    "IEC" AS supplier_iec,
    AVG("UNIT PRICE_INR") AS avg_unit_price,
    EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD'))::INT AS year
FROM shipments
GROUP BY "Model Name", "Model Number", "IEC", year
ORDER BY "Model Name", "Model Number", year;

-- Aggregate total quantity per capacity
SELECT 
    "Capacity" AS capacity,
    SUM("Qty") AS total_quantity
FROM shipments
GROUP BY "Capacity"
ORDER BY total_quantity DESC;

-- Flag duty anomalies (> 2 std dev from mean)
WITH stats AS (
    SELECT 
        AVG("DUTY PAID_INR" / "TOTAL VALUE_INR") AS mean_duty,
        STDDEV("DUTY PAID_INR" / "TOTAL VALUE_INR") AS std_duty
    FROM shipments
)
SELECT s.*,
       ("DUTY PAID_INR" / "TOTAL VALUE_INR") AS duty_percentage,
       CASE 
           WHEN ("DUTY PAID_INR" / "TOTAL VALUE_INR") > mean_duty + 2*std_duty
             OR ("DUTY PAID_INR" / "TOTAL VALUE_INR") < mean_duty - 2*std_duty 
           THEN 'Anomaly'
           ELSE 'Normal'
       END AS duty_flag
FROM shipments s, stats;
