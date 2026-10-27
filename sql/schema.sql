PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS ev_market (
 record_id INTEGER PRIMARY KEY AUTOINCREMENT,
 vehicle_id TEXT NOT NULL,
 model_name TEXT, manufacturer TEXT, model_year INTEGER,
 manufacturing_country TEXT, market_region TEXT, category TEXT,
 battery_capacity_kwh REAL, battery_type TEXT, battery_cycle_life REAL,
 battery_degradation_pct_5yr REAL, range_km REAL, efficiency_wh_per_km REAL,
 motor_power_kw REAL, torque_nm REAL, num_motors INTEGER, drivetrain TEXT,
 top_speed_kmph REAL, acceleration_0_100_sec REAL, max_dc_charging_kw REAL,
 charging_dc_fast_time_min REAL, charging_ac_time_hr REAL, num_charging_ports INTEGER,
 num_seats INTEGER, weight_kg REAL, cargo_capacity_liters REAL, price_usd REAL,
 insurance_cost_usd_yearly REAL, warranty_years INTEGER, resale_value_pct_3yr REAL,
 safety_rating_stars INTEGER, autonomous_level INTEGER, infotainment_screen_inch REAL,
 co2_saved_tons_per_year REAL, annual_sales_units REAL, customer_rating REAL,
 recommended_use_case TEXT, source_split TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ev_market_test (
 record_id INTEGER PRIMARY KEY AUTOINCREMENT,
 vehicle_id TEXT NOT NULL,
 model_name TEXT, manufacturer TEXT, model_year INTEGER,
 manufacturing_country TEXT, market_region TEXT, category TEXT,
 battery_capacity_kwh REAL, battery_type TEXT, battery_cycle_life REAL,
 battery_degradation_pct_5yr REAL, range_km REAL, efficiency_wh_per_km REAL,
 motor_power_kw REAL, torque_nm REAL, num_motors INTEGER, drivetrain TEXT,
 top_speed_kmph REAL, acceleration_0_100_sec REAL, max_dc_charging_kw REAL,
 charging_dc_fast_time_min REAL, charging_ac_time_hr REAL, num_charging_ports INTEGER,
 num_seats INTEGER, weight_kg REAL, cargo_capacity_liters REAL, price_usd REAL,
 insurance_cost_usd_yearly REAL, warranty_years INTEGER, resale_value_pct_3yr REAL,
 safety_rating_stars INTEGER, autonomous_level INTEGER, infotainment_screen_inch REAL,
 co2_saved_tons_per_year REAL, annual_sales_units REAL, customer_rating REAL,
 recommended_use_case TEXT, source_split TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ev_manufacturer ON ev_market(manufacturer);
CREATE INDEX IF NOT EXISTS idx_ev_category ON ev_market(category);
CREATE INDEX IF NOT EXISTS idx_ev_country ON ev_market(manufacturing_country);
CREATE INDEX IF NOT EXISTS idx_ev_year ON ev_market(model_year);
CREATE INDEX IF NOT EXISTS idx_ev_battery ON ev_market(battery_type);
CREATE INDEX IF NOT EXISTS idx_ev_test_manufacturer ON ev_market_test(manufacturer);
CREATE INDEX IF NOT EXISTS idx_ev_test_category ON ev_market_test(category);
