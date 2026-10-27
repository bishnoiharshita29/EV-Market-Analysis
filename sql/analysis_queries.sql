-- Dashboard table ev_market is the cleaned training split only.
-- The 100,000-row test split is stored separately in ev_market_test.

-- 1. Source split row counts
SELECT source_split, COUNT(*) AS records FROM ev_market GROUP BY source_split;
SELECT source_split, COUNT(*) AS records FROM ev_market_test GROUP BY source_split;

-- 2. KPI overview (record-level descriptive metrics)
SELECT COUNT(*) AS vehicle_records,
       COUNT(DISTINCT vehicle_id) AS unique_vehicle_ids,
       COUNT(DISTINCT model_name) AS unique_models,
       COUNT(DISTINCT manufacturer) AS manufacturers,
       ROUND(AVG(range_km), 2) AS avg_range_km,
       ROUND(AVG(battery_capacity_kwh), 2) AS avg_battery_kwh,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
       ROUND(AVG(price_usd), 2) AS avg_price_usd
FROM ev_market;

-- 3. Category comparison
SELECT category, COUNT(*) AS records,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(battery_capacity_kwh), 1) AS avg_battery_kwh,
       ROUND(AVG(customer_rating), 2) AS avg_rating,
       ROUND(SUM(annual_sales_units), 0) AS sum_record_sales_units
FROM ev_market GROUP BY category ORDER BY records DESC;

-- 4. Manufacturer portfolio (record-level sales sum must be labelled carefully)
SELECT manufacturer, COUNT(*) AS model_records,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(customer_rating), 2) AS avg_rating,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(SUM(annual_sales_units), 0) AS sum_record_sales_units
FROM ev_market GROUP BY manufacturer ORDER BY model_records DESC LIMIT 15;

-- 5. Battery technology profile
SELECT battery_type, COUNT(*) AS records,
       ROUND(AVG(battery_capacity_kwh), 1) AS avg_capacity_kwh,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(battery_cycle_life), 0) AS avg_cycle_life,
       ROUND(AVG(battery_degradation_pct_5yr), 2) AS avg_5yr_degradation_pct
FROM ev_market GROUP BY battery_type ORDER BY records DESC;

-- 6. Manufacturing footprint
SELECT manufacturing_country, COUNT(*) AS records,
       COUNT(DISTINCT manufacturer) AS manufacturers,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_market GROUP BY manufacturing_country ORDER BY records DESC;

-- 7. Model-year trend
SELECT model_year, COUNT(*) AS model_records,
       ROUND(AVG(annual_sales_units), 0) AS avg_record_sales_units,
       ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_market GROUP BY model_year ORDER BY model_year;

-- 8. Price bands
SELECT CASE WHEN price_usd < 30000 THEN 'Under $30k'
            WHEN price_usd < 60000 THEN '$30k–$60k'
            WHEN price_usd < 100000 THEN '$60k–$100k'
            ELSE '$100k+' END AS price_band,
       COUNT(*) AS records, ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_market GROUP BY price_band ORDER BY records DESC;

-- 9. Data quality checks after preparation
SELECT COUNT(*) AS records,
       SUM(CASE WHEN range_km IS NULL THEN 1 ELSE 0 END) AS missing_range,
       SUM(CASE WHEN price_usd < 0 THEN 1 ELSE 0 END) AS negative_price,
       SUM(CASE WHEN customer_rating < 0 OR customer_rating > 5 THEN 1 ELSE 0 END) AS invalid_rating
FROM ev_market;
