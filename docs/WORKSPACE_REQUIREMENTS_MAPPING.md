# SkillWallet Requirements Mapping

| SkillWallet requirement | Deliverable / evidence | Status |
|---|---|---|
| Collect the dataset | Original train/test CSVs included in project | Done |
| Store data in DB | `data/ev_market.db`, `sql/schema.sql` | Done |
| Perform SQL operations | `sql/analysis_queries.sql` | Done |
| Connect DB with Tableau | Tableau connection instructions in build guide | Manual Tableau step remaining |
| Prepare data for visualization | `src/build_data.py`, data-quality report, aggregate CSVs | Done |
| Number of unique visualizations | Nine worksheet specifications in Tableau guide | Specification ready; create in Tableau |
| Responsive dashboard design | Dashboard layout and responsive instructions; Flask page responsive | Tableau device layouts still need testing |
| Number of scenes in story | Eight-scene storyboard | Specification ready; create in Tableau |
| Amount of data rendered | 199,999 cleaned training rows / 39 fields; test split stored separately | Verified in SQLite |
| Utilization of filters | Five recommended Tableau filters | Configure/test in Tableau |
| Number of calculated fields | Eight recommended calculated fields | Create in Tableau |
| Number of visualizations/graphs | Nine planned Tableau worksheets; six local interactive preview charts | Tableau workbook creation remaining |
| Publish dashboard/story to Tableau Public | Publishing steps and `.env` URL configuration | Requires Tableau Public account/action |
| Embed dashboard and story with Flask | `/dashboard`, `/story` routes support configured URLs | Code prepared; needs published URLs and runtime dependency install |
| Record explanation video | 5–7 minute script and shot list | User must record actual screen/audio |
| Project documentation | `docs/PROJECT_DOCUMENTATION.md` and README | Done |
| Add Demo/GitHub links in SkillWallet | Final published URLs | After publishing/deploying |
