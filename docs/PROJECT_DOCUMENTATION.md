# Project Documentation: Electric Vehicle Market Performance & Insights

## 1. Abstract

This project analyzes electric-vehicle market data to compare vehicle categories, manufacturers, battery technologies, manufacturing countries, driving range, pricing, annual sales units and customer ratings. The solution combines CSV data preparation in Python, SQL storage and querying with SQLite, visualization design in Tableau, and web integration using Flask. A responsive web portal provides local interactive previews and embeds the published Tableau dashboard and story once their public URLs are configured.

## 2. Problem statement

The EV market includes many vehicle types, manufacturers and battery technologies. Stakeholders need a single analytical view to compare performance, understand the competitive landscape, examine manufacturing distribution, and identify patterns in range, price, sales and customer satisfaction. The project turns a large tabular dataset into interactive views and a guided data story.

## 3. Objectives

- Load and validate the supplied EV train/test CSV files.
- Clean inconsistent or missing values and handle duplicate identifiers.
- Store cleaned training records and the held-out test split in separate queryable relational tables.
- Use SQL to calculate KPIs and group-level summaries.
- Create nine unique Tableau visualizations, a responsive dashboard and an eight-scene story.
- Add calculated fields and interactive filters.
- Benchmark local SQL queries and separately test Tableau rendering/filter behavior.
- Embed the published Tableau views in a Flask website.
- Provide reproducible documentation and a concise project demonstration.

## 4. Tools and technologies

- **Python / pandas / NumPy:** data validation, type conversion, missing-value treatment and aggregation.
- **SQLite:** portable relational database for the cleaned table and SQL analysis.
- **Tableau Public:** visual analytics, dashboard, story and public hosting.
- **Flask / HTML / CSS:** web integration and responsive landing page.
- **Plotly:** local interactive preview charts, useful before the Tableau workbook is published.
- **Git / GitHub:** version control and source-code submission.

## 5. Dataset description

The uploaded archive includes `ev_market_train.csv` and `ev_market_test.csv`. The train file has 200,000 rows and the test file has 100,000 rows; both contain 37 columns. Fields describe vehicle identity, model/manufacturer, model year, country/region, category, battery technology and capacity, battery lifespan/degradation, driving range, efficiency, motor/charging specifications, price and insurance, warranty/resale, safety/autonomy, infotainment, estimated CO₂ saved, annual sales units, customer rating and recommended use case.

The training input contains 200,000 rows and the test input 100,000 rows. The training file contains one exact duplicate vehicle ID; it is removed, producing 199,999 training records with unique IDs. The cleaned training table contains the 37 original fields plus `source_split` and generated `record_id` (39 fields total). The test split is stored separately in `ev_market_test` and excluded from dashboard aggregates. Missing numeric values are replaced with column medians except missing `annual_sales_units`, which is set to zero so summed sales are not inflated by an invented median. Missing categorical values become `Unknown`. The cleaned tables contain no null cells.

**Data caveat:** this is a supplied project dataset, not independently validated official market data. Sales totals and sustainability metrics should be described as dataset values, not real-world market totals. The CSV split labels suggest a training/test partition; this project preserves that separation and uses only the training split for dashboard aggregates. Do not use the combined split to claim predictive model performance.

## 6. Methodology

1. Extract the two CSV files from the provided ZIP archive.
2. Read both files and record source row counts, column counts, missing values and duplicate IDs.
3. Add a `source_split` field (`train` / `test`) to preserve provenance.
4. Trim categorical whitespace, normalize empty strings, and coerce numeric columns to numeric types.
5. Remove repeated `vehicle_id` values while retaining the first occurrence.
6. Impute missing numeric values with training-set medians, except missing annual sales are set to zero; impute categorical values with `Unknown`.
7. Clip negative values in non-negative metrics and keep customer/safety ratings within 0–5.
8. Store the cleaned records in SQLite and create indexes for year, manufacturer, category, country and battery type.
9. Run SQL queries to summarize KPIs, category performance, manufacturers, battery mix, sales by model year, country footprint and customer ratings.
10. Build Tableau worksheets and calculated fields, then compose a dashboard and story.
11. Publish Tableau views to Tableau Public and configure Flask embed URLs.
12. Validate the website, query timings, dashboard load, filters and responsive behavior.

## 7. Database design

The main table is `ev_market`. `vehicle_id` is the primary key. Dimension-like fields include `manufacturer`, `category`, `manufacturing_country`, `market_region`, `battery_type`, `drivetrain`, `recommended_use_case` and `model_year`. Numeric measures include `annual_sales_units`, `customer_rating`, `range_km`, `battery_capacity_kwh`, `price_usd`, efficiency, charging and sustainability-related fields. Indexes are created on the most common filter dimensions.

SQL scripts:
- `sql/schema.sql`: table definition and indexes.
- `sql/analysis_queries.sql`: KPI and analytical queries.

## 8. Visual analytics design

The nine worksheets are listed in `TABLEAU_BUILD_GUIDE.md`: KPI overview, category performance, manufacturer sales, customer-rating treemap, sales trend, battery technology share, manufacturing-country map, battery capacity versus range, and price versus range. The dashboard uses a consistent dark/neutral visual system with a restrained EV accent color, descriptive titles, readable tooltips and interactive filters.

The eight story scenes guide a viewer from an overview through category distribution, manufacturer competition, customer ratings, sales trend, battery technology, manufacturing footprint and business recommendations. Each scene should include a short evidence-based caption and should not claim causation from correlation.

## 9. Performance testing

The data-building script writes `outputs/performance_benchmark.json`, which includes local SQLite query timings. These results are not a substitute for Tableau rendering benchmarks. Before submission, record the following real measurements from the machine used for the demonstration:

| Test | How to measure | Result to enter |
|---|---|---|
| Data rendered | Row count in Tableau data source and marks in charts | 199,999 training rows; 100,000 test rows stored separately; note marks per view |
| Dashboard load | Time from opening published view until charts are usable; repeat 3 times | Enter measured median |
| Filter responsiveness | Change one filter, then several filters; time update | Enter measured median |
| Filter count | Count visible interactive filters | Recommended 5 |
| Calculated fields | Count fields created in Tableau | Recommended 8 |
| Unique visualizations | Count distinct worksheets/chart views | 9 planned |
| Responsive layout | Test desktop and narrow/mobile viewport | Pass/fail with notes |

Do not fill the measurement cells with estimates or invented performance claims.

## 10. Flask web integration

The Flask application exposes:
- `/` — landing page, dataset KPIs and interactive Plotly previews.
- `/dashboard` — published Tableau dashboard embed or setup instructions.
- `/story` — published Tableau story embed or setup instructions.
- `/about` — data preparation and limitations.
- `/health` — JSON health/configuration status.

Set `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL` in `.env` after publishing. Tableau Public URLs must be publicly accessible. The Flask app can run locally; public deployment requires a hosting provider and a configured production server.

## 11. Run instructions

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python src/build_data.py
cp .env.example .env        # Windows: copy .env.example .env
python app.py
```

Visit `http://127.0.0.1:5000`. To verify the application status, open `http://127.0.0.1:5000/health`.

## 12. Conclusion

The project provides a reproducible pipeline from large CSV files to a cleaned SQL table, descriptive summaries, an interactive web portal and a specification for Tableau dashboards/storytelling. It supports comparison of EV categories, manufacturers, batteries and manufacturing locations. The main deliverables are prepared locally; Tableau workbook creation/publication and screen recording must be completed in the relevant desktop applications before claiming the project is fully published.

## 13. Submission checklist

- [ ] Verify the source files and data-quality report.
- [ ] Run `python src/build_data.py` successfully.
- [ ] Execute and verify the SQL queries.
- [ ] Create all nine Tableau worksheets.
- [ ] Create at least six (recommended eight) calculated fields.
- [ ] Configure at least four interactive filters and test combined selections.
- [ ] Assemble responsive dashboard layouts.
- [ ] Create and navigate all eight Tableau story scenes.
- [ ] Record real Tableau load/filter performance results.
- [ ] Publish dashboard and story to Tableau Public.
- [ ] Configure and verify Flask embeds.
- [ ] Test the web app at desktop and mobile widths.
- [ ] Record the 5–7 minute demo video.
- [ ] Push code and documentation to GitHub.
- [ ] Add real demo and GitHub URLs to SkillWallet.
