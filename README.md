# EV-Market-Analysis: EV Market Performance & Insights

A reproducible project using Python, pandas, SQLite/SQL, Tableau Public, Plotly, and Flask. It profiles the supplied EV dataset, stores cleaned training and test records separately, exports group-level summaries, provides an interactive local web preview, and supports Tableau Public dashboard/story embedding.

## Contact
- GitHub: [@bishnoiharshita29](https://github.com/bishnoiharshita29)
- Email: bishnoiharshita880@gmail.com

## Project contents
- `data/ev_market_train.csv` and `data/ev_market_test.csv`: supplied CSV files.
- `src/build_data.py`: cleans data, creates SQLite tables, exports nine analysis aggregates, writes quality/performance reports.
- `src/validate_project.py`: checks row counts, null handling, database schema and aggregate outputs.
- `sql/schema.sql`: SQLite tables and indexes.
- `sql/analysis_queries.sql`: SQL examples for KPI and group-level analysis.
- `outputs/`: generated aggregate CSVs, quality report, query benchmark and validation results.
- `app.py`, `templates/`, `static/`: responsive Flask site with Plotly previews and optional Tableau embeds.
- `docs/PROJECT_DOCUMENTATION.md`: full project report.
- `docs/TABLEAU_BUILD_GUIDE.md`: nine worksheet specifications, calculated fields, dashboard/story and filters.
- `docs/WORKSPACE_REQUIREMENTS_MAPPING.md`: maps each SkillWallet requirement to its evidence and remaining actions.
- `docs/DEMO_VIDEO_SCRIPT.md`: 5–7 minute end-to-end recording script.
- `docs/performance_test.md`: actual Tableau performance log template.

## Quick start
Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python src/build_data.py
python src/validate_project.py
cp .env.example .env                     # Windows: copy .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`. The `/health` route reports whether the local database and Tableau URLs are configured.

## Tableau workflow
1. Run the build script. It cleans the training split (199,999 rows after removing one duplicate ID) and stores the 100,000 test rows separately. Dashboard aggregate files are built from the cleaned training split only.
2. In Tableau Desktop/Public, connect to `data/ev_market.db` if your version supports SQLite, or export the `ev_market` table to CSV using the snippet in `docs/TABLEAU_BUILD_GUIDE.md`.
3. Build the nine sheets, one dashboard and eight story points described in the guide. Add and test the filters/calculated fields.
4. Publish the workbook/story using **File → Save to Tableau Public**.
5. Put the published dashboard/story URLs into `.env` as `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL`, then restart Flask.

## Important data caveat
The supplied dataset has not been independently verified against official market data. `annual_sales_units` is a record-level field; row sums are not verified global or country market totals. Use the charts as exploratory analysis of the supplied records and avoid unsupported causal claims.

## Submission actions still requiring your account/device
You must publish the Tableau workbook/story, copy the public URLs, optionally deploy the Flask app, enter those links in SkillWallet, and record/upload the actual 5–7 minute screen-share video. Do not mark those items complete until verified.
