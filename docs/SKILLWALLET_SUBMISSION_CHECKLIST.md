# SkillWallet Submission Checklist — EV Market Performance & Insights

Status legend: **Prepared/verified locally** means the project files or data checks exist. **Manual Tableau/account action** means you still need to do that step in Tableau Public, SkillWallet, or a screen recorder before marking it complete.

| SkillWallet requirement | Evidence / action | Status |
|---|---|---|
| Collect the dataset | `data/ev_market_train.csv` (200,000 rows) and `data/ev_market_test.csv` (100,000 rows) | Included |
| Store data in DB | `src/build_data.py` creates `data/ev_market.db` with training and test tables | Built and verified locally; regenerate with script |
| Perform SQL operations | `sql/schema.sql`, `sql/analysis_queries.sql`; SQL counts and grouped queries validated | Prepared and locally validated |
| Connect DB with Tableau | Use `data/ev_market.db` if supported or run `python src/export_clean_csv.py` and connect to `outputs/ev_market_clean.csv` | Manual Tableau step remaining |
| Prepare data for visualization | `src/build_data.py`, `outputs/data_quality_report.json`, and 9 aggregate CSVs | Built and verified locally |
| Number of unique visualizations | Build the 9 worksheets in `docs/TABLEAU_BUILD_GUIDE.md` | Specification ready; create in Tableau |
| Responsive dashboard design | Tableau dashboard layout in guide; Flask website has responsive CSS | Website code prepared; test final Tableau layout on desktop and mobile |
| Number of story scenes | 8 scenes specified in Tableau guide | Story plan ready; create in Tableau |
| Amount of data rendered | 199,999 cleaned training rows / 39 fields; 100,000 test rows stored separately | Verified in SQLite; confirm in Tableau |
| Utilization of filters | Recommended filters: year, category, manufacturer, country, battery type | Configure and test in Tableau; use at least 4–5 |
| Number of calculated fields | 8 formulas in Tableau guide | Formulas ready; create in Tableau |
| Number of visualizations/graphs | 9 planned Tableau worksheets; 6 local Plotly preview charts | Preview assets ready; verify Tableau sheet count |
| Publish dashboard/story to Tableau Public | Publish workbook/story and copy their public view URLs | Requires Tableau Public account/action |
| Embed dashboard and story with Flask | `/dashboard` and `/story` use configured URLs in `.env` | Code prepared; requires published URLs and dependencies installed |
| Record explanation video | Follow `docs/DEMO_VIDEO_SCRIPT.md` for a 5–7 minute walkthrough | You must record and upload actual video |
| Project documentation | `docs/PROJECT_DOCUMENTATION.md`, `docs/TABLEAU_BUILD_GUIDE.md`, README, test log | Prepared; update with actual Tableau URLs/timings |
| Demo link | Add a working public Flask deployment or other stable demo | Deploy and test before submission |
| GitHub link | Push project folder to GitHub and paste repository URL | Requires your GitHub account |

## Recommended completion order
1. Run `python src/build_data.py` and `python src/validate_project.py`.
2. Build all nine Tableau worksheets.
3. Create the dashboard and test at least four filters, including three simultaneous filters.
4. Create all eight Story scenes.
5. Publish the workbook/story to Tableau Public.
6. Add the published URLs to `.env` and verify Flask embeds.
7. Fill the performance test log using real Tableau timings (do not estimate).
8. Record and upload the 5–7 minute demo video.
9. Push the code and docs to GitHub and test the demo URL while signed out.
10. Update SkillWallet statuses only after each item is actually complete.
