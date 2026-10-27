"""Build a train-only Tableau analysis table plus a separately preserved test table."""
from pathlib import Path
import json, sqlite3, time
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=ROOT/'outputs'; SQL=ROOT/'sql'
DATA.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
TRAIN_PATH=DATA/'ev_market_train.csv'; TEST_PATH=DATA/'ev_market_test.csv'
NUMERIC=['model_year','battery_capacity_kwh','battery_cycle_life','battery_degradation_pct_5yr','range_km','efficiency_wh_per_km','motor_power_kw','torque_nm','num_motors','top_speed_kmph','acceleration_0_100_sec','max_dc_charging_kw','charging_dc_fast_time_min','charging_ac_time_hr','num_charging_ports','num_seats','weight_kg','cargo_capacity_liters','price_usd','insurance_cost_usd_yearly','warranty_years','resale_value_pct_3yr','safety_rating_stars','autonomous_level','infotainment_screen_inch','co2_saved_tons_per_year','annual_sales_units','customer_rating']
CATEGORICAL=['model_name','manufacturer','manufacturing_country','market_region','category','battery_type','drivetrain','recommended_use_case']
NONNEGATIVE=['battery_capacity_kwh','battery_cycle_life','battery_degradation_pct_5yr','range_km','efficiency_wh_per_km','motor_power_kw','torque_nm','top_speed_kmph','acceleration_0_100_sec','max_dc_charging_kw','charging_dc_fast_time_min','charging_ac_time_hr','weight_kg','cargo_capacity_liters','price_usd','insurance_cost_usd_yearly','co2_saved_tons_per_year','annual_sales_units']

def prep(path, split, medians=None):
    df=pd.read_csv(path,low_memory=False)
    stats={'file':path.name,'rows':len(df),'columns':len(df.columns),'missing_cells':int(df.isna().sum().sum()),'duplicate_vehicle_ids':int(df.vehicle_id.duplicated().sum())}
    df['source_split']=split
    for c in CATEGORICAL: df[c]=df[c].astype('string').str.strip().replace('',pd.NA)
    for c in NUMERIC: df[c]=pd.to_numeric(df[c],errors='coerce')
    df['model_year']=df['model_year'].round().astype('Int64')
    # The train file has one exact duplicate vehicle row; remove duplicate IDs from the analysis table.
    duplicate_ids=int(df.vehicle_id.duplicated(keep='first').sum())
    df=df.drop_duplicates(subset=['vehicle_id'],keep='first').copy()
    missing_before=int(df.isna().sum().sum())
    if medians is None: medians={c:df[c].median() for c in NUMERIC}
    for c in NUMERIC:
        if df[c].isna().any():
            # Missing sales are set to zero to avoid inflating summed sales with an invented median.
            fill_value=0 if c=='annual_sales_units' else medians[c]
            df[c]=df[c].fillna(fill_value)
    for c in CATEGORICAL: df[c]=df[c].fillna('Unknown').astype(str)
    df['model_year']=df['model_year'].astype(int); df['vehicle_id']=df['vehicle_id'].astype(str)
    for c in NONNEGATIVE: df[c]=df[c].clip(lower=0)
    df['customer_rating']=df['customer_rating'].clip(0,5); df['safety_rating_stars']=df['safety_rating_stars'].clip(0,5)
    return df,stats,duplicate_ids,missing_before,medians

def main():
    start=time.perf_counter()
    if not TRAIN_PATH.exists() or not TEST_PATH.exists(): raise FileNotFoundError('Place both ev_market_train.csv and ev_market_test.csv in the project root.')
    train,train_stats,dup_train,missing_train,medians=prep(TRAIN_PATH,'train')
    test,test_stats,dup_test,missing_test,_=prep(TEST_PATH,'test',medians)
    db=DATA/'ev_market.db'
    if db.exists(): db.unlink()
    con=sqlite3.connect(db); con.executescript((SQL/'schema.sql').read_text())
    # Surrogate record_id is the primary key; vehicle_id remains a business identifier.
    train.to_sql('ev_market',con,if_exists='append',index=False,chunksize=500,method='multi')
    test.to_sql('ev_market_test',con,if_exists='append',index=False,chunksize=500,method='multi')
    con.commit()
    # All dashboard aggregates use the cleaned training split, matching the 200k-row source used by the brief.
    aggs={
      'category_performance':train.groupby('category').agg(model_count=('vehicle_id','count'),annual_sales_units=('annual_sales_units','sum'),avg_range_km=('range_km','mean'),avg_rating=('customer_rating','mean'),avg_price_usd=('price_usd','mean')).reset_index().sort_values('annual_sales_units',ascending=False),
      'manufacturer_performance':train.groupby('manufacturer').agg(model_count=('vehicle_id','count'),annual_sales_units=('annual_sales_units','sum'),avg_rating=('customer_rating','mean'),avg_range_km=('range_km','mean')).reset_index().sort_values('annual_sales_units',ascending=False),
      'battery_mix':train.groupby('battery_type').agg(model_count=('vehicle_id','count'),avg_capacity_kwh=('battery_capacity_kwh','mean'),avg_range_km=('range_km','mean'),avg_cycle_life=('battery_cycle_life','mean'),avg_degradation_pct=('battery_degradation_pct_5yr','mean')).reset_index().sort_values('model_count',ascending=False),
      'sales_by_year':train.groupby('model_year').agg(annual_sales_units=('annual_sales_units','sum'),model_records=('vehicle_id','count')).reset_index().sort_values('model_year'),
      'country_footprint':train.groupby('manufacturing_country').agg(model_count=('vehicle_id','count'),annual_sales_units=('annual_sales_units','sum'),avg_rating=('customer_rating','mean')).reset_index().sort_values('model_count',ascending=False),
      'rating_by_category':train.groupby('category').agg(avg_rating=('customer_rating','mean'),rated_records=('customer_rating','count')).reset_index().sort_values('avg_rating',ascending=False),
      'region_performance':train.groupby('market_region').agg(model_count=('vehicle_id','count'),annual_sales_units=('annual_sales_units','sum'),avg_range_km=('range_km','mean'),avg_rating=('customer_rating','mean')).reset_index(),
      'price_range_by_category':train.groupby('category').agg(avg_price_usd=('price_usd','mean'),avg_range_km=('range_km','mean'),avg_efficiency_wh_per_km=('efficiency_wh_per_km','mean')).reset_index(),
      'use_case_mix':train.groupby('recommended_use_case').agg(model_count=('vehicle_id','count'),annual_sales_units=('annual_sales_units','sum'),avg_rating=('customer_rating','mean')).reset_index().sort_values('model_count',ascending=False),
    }
    for name,df in aggs.items(): df.to_csv(OUT/f'{name}.csv',index=False,float_format='%.3f')
    kpis={'rows_train':train_stats['rows'],'rows_test':test_stats['rows'],'source_columns':len(train.columns)-1,'train_rows_after_dedup':len(train),'test_rows_stored':len(test),'cleaned_rows':len(train),'duplicate_ids_removed_from_train':dup_train,'duplicate_ids_removed_from_test':dup_test,'missing_cells_before_imputation':missing_train,'missing_cells_after_cleaning':int(train.isna().sum().sum()),'unique_models':int(train.model_name.nunique()),'unique_vehicle_ids':int(train.vehicle_id.nunique()),'unique_manufacturers':int(train.manufacturer.nunique()),'unique_categories':int(train.category.nunique()),'unique_countries':int(train.manufacturing_country.nunique()),'unique_battery_types':int(train.battery_type.nunique()),'avg_customer_rating':round(float(train.customer_rating.mean()),3),'avg_range_km':round(float(train.range_km.mean()),3),'avg_battery_capacity_kwh':round(float(train.battery_capacity_kwh.mean()),3),'total_annual_sales_units':round(float(train.annual_sales_units.sum()),2),'database_mb':round(db.stat().st_size/1024/1024,2),'build_seconds':round(time.perf_counter()-start,2),'source_stats':[train_stats,test_stats],'analysis_scope':'cleaned training split only; test split stored separately and excluded from dashboard aggregates'}
    (OUT/'data_quality_report.json').write_text(json.dumps(kpis,indent=2))
    tests=[]
    for label,query in [('KPI query','SELECT COUNT(*),COUNT(DISTINCT manufacturer),AVG(customer_rating) FROM ev_market'),('Grouped category query','SELECT category,SUM(annual_sales_units) FROM ev_market GROUP BY category'),('Multi-filter query',"SELECT COUNT(*) FROM ev_market WHERE model_year >= 2022 AND category='Electric SUV' AND manufacturing_country='India'")]:
        t=time.perf_counter(); con.execute(query).fetchall(); elapsed=(time.perf_counter()-t)*1000
        tests.append({'test':label,'elapsed_ms':round(elapsed,2),'status':'PASS' if elapsed<2000 else 'REVIEW'})
    (OUT/'performance_benchmark.json').write_text(json.dumps({'rows_in_dashboard_table':len(train),'test_rows_stored_separately':len(test),'database_mb':kpis['database_mb'],'query_tests':tests,'note':'Local SQLite query timings; Tableau rendering and filter responsiveness must be timed in Tableau Desktop/Public.'},indent=2))
    con.close(); print(json.dumps(kpis,indent=2)); print('Aggregate files:',len(aggs))
if __name__=='__main__': main()
