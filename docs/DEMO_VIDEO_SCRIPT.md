# 5–7 Minute End-to-End Demo Script

Target duration: approximately 6 minutes. Record your actual screen and voice; this script is a guide, not a completed video.

## 0:00–0:35 — Introduction
“Hello, this is my Electric Vehicle Market Performance and Insights project. The goal is to explore the supplied EV records across vehicle categories, manufacturers, battery technologies, range, price, customer ratings, and manufacturing geography. The project uses Python for data preparation, SQLite for SQL analysis, Tableau for interactive visualization, and Flask for web integration.”

## 0:35–1:20 — Dataset and profiling
Show the source CSV files and run `python src/build_data.py`. Explain that the archive has 200,000 training rows and 100,000 test rows, 37 columns per file, and missing values. Mention that one duplicate vehicle ID is removed from the training analysis table and the test split is stored separately.

## 1:20–2:05 — Data preparation and SQL
Run `python src/build_data.py`, then `python src/validate_project.py`. Open `sql/analysis_queries.sql` and explain the category, manufacturer, battery, country, and year aggregations. Show the database row count and at least one query result. Note that sales-unit sums are record-level and not verified market totals.

## 2:05–3:50 — Tableau worksheets and dashboard
Open the workbook in Tableau. Show the KPI overview, category distribution, manufacturer comparison, rating chart, year trend, battery mix, range-versus-capacity scatter, country distribution, and price-versus-range trade-off. Open the dashboard and demonstrate manufacturer, category, battery, country, year, and source-split filters. Apply multiple filters together and reset them.

## 3:50–4:45 — Tableau Story
Navigate through the eight story scenes: overview, categories, manufacturers, ratings, year patterns, battery technology, manufacturing footprint, and business implications. Explain one evidence-based takeaway per scene and avoid implying causation.

## 4:45–5:35 — Flask integration
Run `python app.py` and open `http://127.0.0.1:5000`. Show the landing page and local preview. If Tableau has been published, show the actual embedded dashboard and story after setting the two URLs in `.env`. Test the page at a narrow window width.

## 5:35–6:15 — Testing and conclusion
Show the performance test log with real timing measurements. Summarize the deliverables and explain that the analysis is based on the supplied dataset and should be interpreted as descriptive. End by showing the GitHub repository and published Tableau links.

## Recording checklist
- [ ] Screen-share at readable zoom; close unrelated tabs and notifications.
- [ ] Speak clearly and keep the recording between 5 and 7 minutes.
- [ ] Include the problem statement, preprocessing, SQL, dashboard, story, and key insights.
- [ ] Show actual working filters and a published embed if completed.
- [ ] Save video as MP4 and upload to the requested submission location.
