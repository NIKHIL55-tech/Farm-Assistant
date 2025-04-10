import sys
import pandas as pd
from core.weather_integration import WeatherIntegration

def test_initialization():
    print("Testing application initialization...")
    
    try:
        # Check weather integration
        weather = WeatherIntegration()
        locations = list(weather.weather_stations.keys())
        print(f"Weather locations found: {locations}")
        
        # Check farm data
        farm_data = pd.read_csv("data/farmer_advisor_dataset.csv")
        print(f"Farm data columns: {farm_data.columns.tolist()}")
        
        # Check if there's crop data
        crops = farm_data['Crop_Type'].unique().tolist()
        print(f"Crops found: {crops[:5]}...")
        
        # Check if soil type exists
        if 'Soil_Type' in farm_data.columns:
            soil_types = farm_data['Soil_Type'].unique().tolist()
            print(f"Soil types found: {soil_types[:5]}...")
        else:
            print("'Soil_Type' not found in dataset, using default values")
        
        # Check if irrigation type exists
        if 'Irrigation_Type' in farm_data.columns:
            irrigation_types = farm_data['Irrigation_Type'].unique().tolist()
            print(f"Irrigation types found: {irrigation_types[:5]}...")
        else:
            irrigation_types = ['Drip', 'Sprinkler', 'Flood', 'Furrow']
            print(f"'Irrigation_Type' not found in dataset, using default values: {irrigation_types}")
        
        print("All checks passed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_initialization()
    sys.exit(0 if success else 1) 