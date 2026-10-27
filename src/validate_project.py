"""Sanity checks for generated EV analysis assets."""
from pathlib import Path
import json, sqlite3, sys
ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'outputs'/'data_quality_report.json').read_text())
assert report['rows_train']==200000
assert report['rows_test']==100000
assert report['cleaned_rows']==199999
assert report['source_columns']==37
assert report['missing_cells_after_cleaning']==0
with sqlite3.connect(ROOT/'data'/'ev_market.db') as con:
    n=con.execute('SELECT COUNT(*) FROM ev_market').fetchone()[0]
    nt=con.execute('SELECT COUNT(*) FROM ev_market_test').fetchone()[0]
    nulls=con.execute('SELECT COUNT(*) FROM ev_market WHERE vehicle_id IS NULL OR manufacturer IS NULL OR category IS NULL').fetchone()[0]
    test_nulls=con.execute('SELECT COUNT(*) FROM ev_market_test WHERE vehicle_id IS NULL OR manufacturer IS NULL OR category IS NULL').fetchone()[0]
    ids=con.execute('SELECT COUNT(DISTINCT vehicle_id) FROM ev_market').fetchone()[0]
assert n==199999 and nt==100000 and ids==n and nulls==0 and test_nulls==0
expected=['category_performance','manufacturer_performance','battery_mix','sales_by_year','country_footprint','rating_by_category','region_performance','price_range_by_category','use_case_mix']
for name in expected: assert (ROOT/'outputs'/f'{name}.csv').exists(),name
print('PASS: train/test split counts, unique train IDs, null check, and 9 aggregate files verified.')
