import sqlite3
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "agro_system.db")
FARM_DATA_PATH = os.path.join(BASE_DIR, "data", "farmer_advisor_dataset.csv")
MARKET_DATA_PATH = os.path.join(BASE_DIR, "data", "market_researcher_dataset.csv")

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop existing tables (to avoid schema mismatch)
cursor.execute("DROP TABLE IF EXISTS farms")
cursor.execute("DROP TABLE IF EXISTS markets")

# Create farms table
cursor.execute('''
CREATE TABLE farms (
    Farm_ID INTEGER,
    Soil_pH REAL,
    Soil_Moisture REAL,
    Temperature_C REAL,
    Rainfall_mm REAL,
    Crop_Type TEXT,
    Fertilizer_Usage_kg REAL,
    Pesticide_Usage_kg REAL,
    Crop_Yield_ton REAL,
    Sustainability_Score REAL
)
''')

# Create markets table
cursor.execute('''
CREATE TABLE markets (
    Market_ID INTEGER,
    Product TEXT,
    Market_Price_per_ton REAL,
    Demand_Index REAL,
    Supply_Index REAL,
    Competitor_Price_per_ton REAL,
    Economic_Indicator REAL,
    Weather_Impact_Score REAL,
    Seasonal_Factor REAL,
    Consumer_Trend_Index REAL
)
''')

# Load CSV data
df_farms = pd.read_csv(FARM_DATA_PATH)
df_markets = pd.read_csv(MARKET_DATA_PATH)

# Insert data into tables
df_farms.to_sql("farms", conn, if_exists="append", index=False)
df_markets.to_sql("markets", conn, if_exists="append", index=False)

# Finalize and close connection
conn.commit()
conn.close()

print("✅ Database initialized and datasets imported successfully.")
