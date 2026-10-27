"""Export the cleaned SQLite table to a CSV for Tableau versions without SQLite support."""
from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
with sqlite3.connect(ROOT/'data'/'ev_market.db') as con:
    pd.read_sql_query('SELECT * FROM ev_market',con).to_csv(ROOT/'outputs'/'ev_market_clean.csv',index=False)
print('Wrote outputs/ev_market_clean.csv')
