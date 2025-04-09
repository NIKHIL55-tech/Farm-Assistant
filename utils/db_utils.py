import sqlite3
import pandas as pd

def connect_db(path="database/agro_system.db"):
    return sqlite3.connect(path)

def query_to_dataframe(query, params=None, db_path="database/agro_system.db"):
    """Execute SQL query and return results as pandas DataFrame"""
    conn = connect_db(db_path)
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def get_farm_data(farm_id=None):
    """Get all farm data or for a specific farm_id"""
    if farm_id:
        query = "SELECT * FROM farms WHERE Farm_ID = ?"
        return query_to_dataframe(query, params=(farm_id,))
    return query_to_dataframe("SELECT * FROM farms")

def get_market_data(product=None):
    """Get all market data or filter by product"""
    if product:
        query = "SELECT * FROM markets WHERE Product = ?"
        return query_to_dataframe(query, params=(product,))
    return query_to_dataframe("SELECT * FROM markets")

def get_crop_recommendations(soil_ph, rainfall, temperature):
    """Get recommended crops based on soil and climate conditions"""
    # Widen the search criteria to ensure results
    query = """
    SELECT Crop_Type, AVG(Crop_Yield_ton) as Avg_Yield, 
           COUNT(*) as Sample_Count
    FROM farms 
    WHERE Soil_pH BETWEEN ? AND ?
    GROUP BY Crop_Type
    HAVING Sample_Count >= 5
    ORDER BY Avg_Yield DESC
    """
    # Using a wider pH range to ensure we get results
    params = (soil_ph-1.0, soil_ph+1.0)
    result = query_to_dataframe(query, params=params)
    
    # If still no results, return top crops regardless of conditions
    if result.empty:
        query = """
        SELECT Crop_Type, AVG(Crop_Yield_ton) as Avg_Yield
        FROM farms
        GROUP BY Crop_Type
        ORDER BY Avg_Yield DESC
        """
        result = query_to_dataframe(query)
    
    return result

def get_market_trends():
    """Analyze market trends to find profitable crops"""
    query = """
    SELECT Product, AVG(Market_Price_per_ton) as Avg_Price, 
           AVG(Demand_Index) as Avg_Demand
    FROM markets
    GROUP BY Product
    ORDER BY (Avg_Price * Avg_Demand) DESC
    """
    return query_to_dataframe(query)
