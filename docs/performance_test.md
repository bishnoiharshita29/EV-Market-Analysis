# Performance Testing Log

The build script already records **local SQLite query timings** in `outputs/performance_benchmark.json`. Those are not Tableau render timings. Fill the table below while testing the actual Tableau workbook; do not invent timing values.

## Environment
- Device / CPU / RAM: ______________________________
- Operating system: ________________________________
- Tableau Desktop/Public version: __________________
- Browser (if published): __________________________
- Connection type: _________________________________
- Tableau data-source row count: ___________________
- Workbook size: ___________________________________

## Requirement counts
| Metric | Target / expected | Actual (fill after final build) |
|---|---:|---:|
| Unique visualization worksheets | 9 | ___ |
| Dashboard | 1 | ___ |
| Story scenes | 8 | ___ |
| Calculated fields | 8 recommended | ___ |
| Visible interactive filters | 4–5 minimum/recommended | ___ |
| Cleaned training rows | 199,999 | ___ |
| Test rows stored separately | 100,000 | ___ |

## Timings (seconds)
| Action | Run 1 | Run 2 | Run 3 | Median |
|---|---:|---:|---:|---:|
| Initial dashboard load | ___ | ___ | ___ | ___ |
| Apply one filter | ___ | ___ | ___ | ___ |
| Apply three simultaneous filters | ___ | ___ | ___ | ___ |
| Reset filters | ___ | ___ | ___ | ___ |
| Open a story scene | ___ | ___ | ___ | ___ |

## Pass/fail checklist
- [ ] Initial dashboard loads without errors.
- [ ] All nine sheets render with meaningful titles and units.
- [ ] All eight story points load in sequence.
- [ ] At least four filters are visible and functional.
- [ ] Three filters can be applied simultaneously without broken views.
- [ ] KPI values match SQL results for the same training split and aggregation.
- [ ] Null/unknown handling is intentional and documented.
- [ ] Dashboard tested at desktop and narrow/mobile widths.
- [ ] Tableau Public views load from Flask after URL configuration.

## Notes / bottlenecks
Record slow sheets, filter behavior, and changes made to improve them:

____________________________________________________________________

____________________________________________________________________
