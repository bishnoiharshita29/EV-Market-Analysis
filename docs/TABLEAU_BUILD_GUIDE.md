# Tableau Build Guide — EV Market Performance & Insights

## 1. Connect and validate

Recommended analysis table: `ev_market` in `data/ev_market.db`. It contains the 37 original CSV fields plus `source_split` and generated `record_id` (39 fields total), with 199,999 cleaned training rows after removing one exact duplicate `vehicle_id`. The 100,000-row test split is stored separately in `ev_market_test` and excluded from dashboard aggregates. If your Tableau installation has no SQLite connector, export `ev_market` to a CSV using Python:

```python
import sqlite3, pandas as pd
with sqlite3.connect('data/ev_market.db') as con:
    pd.read_sql_query('SELECT * FROM ev_market', con).to_csv('outputs/ev_market_clean.csv', index=False)
```

In Tableau, verify row count = 199,999 and field count = 39. Set geographic role of `manufacturing_country` to Country/Region. Check `model_year` is a whole number and all numeric measures have numeric data types.

## 2. Nine unique visualizations

Create each as a separate worksheet; use meaningful titles and informative tooltips.

| # | Worksheet title | Chart | Fields / setup |
|---|---|---|---|
| 1 | EV Market Performance at a Glance | KPI cards | COUNTD(vehicle_id), COUNTD(manufacturer), SUM(annual_sales_units), AVG(customer_rating), AVG(range_km), AVG(battery_capacity_kwh) |
| 2 | EV Category Performance & Distribution | Horizontal bar | Rows: `category`; Columns: SUM(`annual_sales_units`); sort descending; label top categories |
| 3 | Market Share by Manufacturer | Horizontal bar / lollipop | Rows: `manufacturer`; Columns: SUM(`annual_sales_units`); sort descending; Top 10 or Top 15 filter |
| 4 | Customer Rating Records by EV Category | Treemap | `category` on Label; COUNT(`vehicle_id`) on Size; AVG(`customer_rating`) on Color/Tooltip |
| 5 | Annual EV Sales Trend by Model Year | Line | Columns: `model_year`; Rows: SUM(`annual_sales_units`); show markers and labels where readable |
| 6 | Battery Technology Market Share | Donut or pie | `battery_type` on Color; COUNT(`vehicle_id`) on Angle/Label; include share percentage |
| 7 | Electric Vehicle Distribution by Manufacturing Country | Filled map | Geographic `manufacturing_country`; Color by COUNT(`vehicle_id`); tooltip sales, rating, range |
| 8 | Battery Capacity vs Driving Range | Scatter plot | X: AVG(`battery_capacity_kwh`); Y: AVG(`range_km`); Color: `battery_type`; Detail: `category`; Size: AVG(`annual_sales_units`) |
| 9 | Price vs Range by Category | Scatter plot | X: AVG(`price_usd`); Y: AVG(`range_km`); Color: `category`; Detail: `manufacturer`; use log price axis only if it improves readability |

Do not use an aggregate CSV as the sole data source for the final dashboard if you need all row-level filter combinations. Use the cleaned `ev_market` table for the workbook; aggregates are for checking results and lightweight previews.

## 3. Calculated fields (create at least 6; recommended 8)

1. **Sales Market Share**
   ```tableau
   SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))
   ```
   Format as percentage. Table calculation direction must be checked for each view.

2. **Range per kWh**
   ```tableau
   IF AVG([battery_capacity_kwh]) > 0 THEN AVG([range_km]) / AVG([battery_capacity_kwh]) END
   ```

3. **Price per km of Range**
   ```tableau
   IF AVG([range_km]) > 0 THEN AVG([price_usd]) / AVG([range_km]) END
   ```

4. **Rating Band**
   ```tableau
   IF [customer_rating] >= 4.5 THEN "Excellent"
   ELSEIF [customer_rating] >= 4.0 THEN "High"
   ELSEIF [customer_rating] >= 3.0 THEN "Moderate"
   ELSE "Low"
   END
   ```

5. **Range Band**
   ```tableau
   IF [range_km] >= 500 THEN "500+ km"
   ELSEIF [range_km] >= 350 THEN "350–499 km"
   ELSEIF [range_km] >= 200 THEN "200–349 km"
   ELSE "Under 200 km"
   END
   ```

6. **Model Age (Years)**
   ```tableau
   YEAR(TODAY()) - [model_year]
   ```
   Interpret as age relative to the current date, not product lifecycle truth.

7. **CO2 Saved per 1,000 Sales**
   ```tableau
   IF SUM([annual_sales_units]) > 0 THEN
     SUM([co2_saved_tons_per_year]) / SUM([annual_sales_units]) * 1000
   END
   ```
   Confirm that the source metric definition supports summing CO₂ saved across models before interpreting it.

8. **Battery Degradation Band**
   ```tableau
   IF [battery_degradation_pct_5yr] < 10 THEN "Low (<10%)"
   ELSEIF [battery_degradation_pct_5yr] < 20 THEN "Medium (10–19.9%)"
   ELSE "High (20%+)"
   END
   ```

## 4. Dashboard layout and filters

Dashboard name: **EV Market Performance & Insights**. Use a fixed desktop canvas around 1366×900 or a range size suitable for your device; enable automatic sizing / device layouts and verify at desktop, tablet, and mobile widths.

Suggested layout:
- Header: title, subtitle, small note that data is provided benchmark data.
- Row 1: six KPI cards (records, manufacturers, sales, rating, range, capacity).
- Row 2: category performance, manufacturer leaders, customer rating treemap.
- Row 3: annual sales trend, battery technology share, manufacturing country map.
- Row 4: battery capacity vs range and price vs range scatter plots.
- Filter rail: Model Year, Category, Manufacturer, Manufacturing Country, Battery Type. Show only the four most useful filters by default if space is limited; retain Battery Type as an additional filter in the dashboard.
- Add a reset-filter instruction or revert button if supported by your Tableau version.

Set filters to **Apply to Worksheets → All Using This Data Source**. Add highlight/filter actions only where they make interpretation clearer. Keep tooltips concise and use consistent number formats.

## 5. Eight-scene Tableau Story

The SkillWallet screenshot's story example includes a multi-scene narrative and the requested metric is “No of Scenes of Story”. Build **8 scenes** with the following names:

1. **EV Market Performance at a Glance** — KPI overview and problem framing.
2. **Understanding EV Category Distribution** — category count and sales contribution.
3. **Leading Manufacturers Driving the EV Market** — top manufacturers by annual sales.
4. **Customer Engagement Across EV Categories** — ratings by category and rating bands.
5. **Growth Trend in Annual EV Sales** — model-year trend; note that model year is not necessarily the actual year of sales.
6. **Battery Technology Market Share** — battery mix, capacity and degradation.
7. **Global EV Manufacturing Footprint** — country-level distribution and region differences.
8. **Key Business Insights & Recommendations** — summary, caveats and actionable implications.

Create each scene using a relevant worksheet/dashboard, add a short caption with one evidence-based takeaway, and ensure the story navigation works. Do not claim causal relationships from descriptive comparisons.

## 6. Performance testing and evidence

The generated `outputs/performance_benchmark.json` measures local SQLite query timings only. For SkillWallet's Tableau performance fields, record actual values from your machine:

- **Amount of Data Rendered:** 199,999 cleaned training rows (39 fields including `source_split`) in the source table; the 100,000-row test split remains separate. Also note the number of marks rendered in individual charts; it will differ by view.
- **Utilization of Filters:** at least 4 visible interactive filters; recommended 5 (year, category, manufacturer, country, battery type).
- **Number of Calculated Fields:** 8 recommended calculated fields above.
- **Number of Visualizations / Graphs:** 9 unique worksheets (KPI panel + 8 chart views; if the evaluator counts only chart types, report the exact number of distinct worksheets and chart types separately).
- Measure dashboard initial load and filter response with a stopwatch, repeat 3 times, and report median. Do not invent timings.
- Test filter combinations: one filter, two filters, and all visible filters at once. Check that values update and no chart goes blank unexpectedly.
- Test responsive layouts at desktop and mobile widths.

## 7. Publish and embed

1. Save the workbook locally.
2. In Tableau Public, choose **File → Save to Tableau Public** and sign in.
3. Give the workbook a clear name, e.g. `EV Market Performance & Insights`.
4. Publish and inspect the dashboard and story in a browser.
5. Copy each view's public URL. Configure `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL` in `.env`.
6. Restart Flask and test `/dashboard` and `/story`.
7. Ensure the published views are accessible without a private account. Public workbooks are publicly viewable; do not publish confidential data.
