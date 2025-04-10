import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import logging

class WeatherIntegration:
    def __init__(self):
        # Simulated weather stations with their baseline climate characteristics
        self.weather_stations = {
            "Karimnagar": {"base_temp": 28, "base_rainfall": 900, "base_humidity": 65, "season_amplitude": 6},
            "Warangal": {"base_temp": 29, "base_rainfall": 850, "base_humidity": 62, "season_amplitude": 7},
            "Nizamabad": {"base_temp": 27, "base_rainfall": 950, "base_humidity": 68, "season_amplitude": 5},
            "Adilabad": {"base_temp": 26, "base_rainfall": 1000, "base_humidity": 70, "season_amplitude": 8},
            "Khammam": {"base_temp": 30, "base_rainfall": 800, "base_humidity": 60, "season_amplitude": 7}
        }
        
        # Crop weather sensitivity (impact of favorable/unfavorable weather on yield)
        self.crop_weather_sensitivity = {
            "Rice": {"temp": 0.8, "rainfall": 1.0, "humidity": 0.7},
            "Wheat": {"temp": 0.9, "rainfall": 0.7, "humidity": 0.5},
            "Corn": {"temp": 0.7, "rainfall": 0.8, "humidity": 0.6},
            "Cotton": {"temp": 0.6, "rainfall": 0.9, "humidity": 0.4},
            "Chickpea": {"temp": 0.8, "rainfall": 0.6, "humidity": 0.5},
            "Soybean": {"temp": 0.7, "rainfall": 0.8, "humidity": 0.6}
        }
        
        # Optimal growing conditions
        self.crop_optimal_conditions = {
            "Rice": {"temp": [24, 30], "rainfall": [1000, 1500], "humidity": [70, 85]},
            "Wheat": {"temp": [15, 24], "rainfall": [750, 900], "humidity": [50, 70]},
            "Corn": {"temp": [20, 28], "rainfall": [800, 1100], "humidity": [60, 75]},
            "Cotton": {"temp": [25, 35], "rainfall": [700, 1000], "humidity": [50, 65]},
            "Chickpea": {"temp": [18, 26], "rainfall": [600, 800], "humidity": [40, 60]},
            "Soybean": {"temp": [22, 30], "rainfall": [800, 1200], "humidity": [55, 70]}
        }
        
        # Initialize random seed for reproducibility
        np.random.seed(42)
    
    def get_historical_weather(self, location, months_back=12):
        """
        Get simulated historical weather data for a location
        
        Parameters:
        - location: Name of the location (must be in weather_stations)
        - months_back: How many months of historical data to generate
        
        Returns:
        - DataFrame with simulated historical weather data
        """
        if location not in self.weather_stations:
            logging.warning(f"Unknown location: {location}. Using default weather patterns.")
            location = next(iter(self.weather_stations))
        
        # Get base values for the location
        base = self.weather_stations[location]
        
        # Generate dates from past to present
        end_date = datetime.datetime.now().replace(day=1)
        start_date = end_date - relativedelta(months=months_back)
        dates = pd.date_range(start=start_date, end=end_date, freq='MS')
        
        # Create weather dataframe
        weather_data = []
        
        for date in dates:
            # Calculate seasonal adjustments (simple sine wave pattern)
            month = date.month
            season_factor = np.sin(np.pi * (month - 3) / 6)  # Peak in July, low in January
            
            # Add some randomness
            temp_random = np.random.normal(0, 1.5)
            rainfall_random = np.random.normal(0, 50)
            humidity_random = np.random.normal(0, 5)
            
            # Calculate weather values with seasonal and random factors
            temp = base["base_temp"] + base["season_amplitude"] * season_factor + temp_random
            rainfall = max(0, base["base_rainfall"] * (1 + 0.3 * season_factor) + rainfall_random)
            humidity = min(100, max(10, base["base_humidity"] + 10 * season_factor + humidity_random))
            
            weather_data.append({
                "date": date,
                "location": location,
                "temperature_C": round(temp, 1),
                "rainfall_mm": round(rainfall, 0),
                "humidity_pct": round(humidity, 0)
            })
        
        return pd.DataFrame(weather_data)
    
    def get_weather_forecast(self, location, months_ahead=3):
        """
        Get simulated weather forecast for a location
        
        Parameters:
        - location: Name of the location (must be in weather_stations)
        - months_ahead: How many months of forecast to generate
        
        Returns:
        - DataFrame with simulated forecast data
        """
        # Use similar logic as historical data but with increased uncertainty
        if location not in self.weather_stations:
            logging.warning(f"Unknown location: {location}. Using default weather patterns.")
            location = next(iter(self.weather_stations))
        
        # Get base values for the location
        base = self.weather_stations[location]
        
        # Generate dates from present to future
        start_date = datetime.datetime.now().replace(day=1) + relativedelta(months=1)
        end_date = start_date + relativedelta(months=months_ahead)
        dates = pd.date_range(start=start_date, end=end_date, freq='MS')
        
        # Create forecast dataframe with increasing uncertainty
        forecast_data = []
        
        for i, date in enumerate(dates):
            # Calculate seasonal adjustments (simple sine wave pattern)
            month = date.month
            season_factor = np.sin(np.pi * (month - 3) / 6)  # Peak in July, low in January
            
            # Add increasing randomness based on how far in the future
            uncertainty_factor = 1 + i * 0.2  # Uncertainty increases with forecast distance
            temp_random = np.random.normal(0, 1.5 * uncertainty_factor)
            rainfall_random = np.random.normal(0, 50 * uncertainty_factor)
            humidity_random = np.random.normal(0, 5 * uncertainty_factor)
            
            # Calculate weather values with seasonal and random factors
            temp = base["base_temp"] + base["season_amplitude"] * season_factor + temp_random
            rainfall = max(0, base["base_rainfall"] * (1 + 0.3 * season_factor) + rainfall_random)
            humidity = min(100, max(10, base["base_humidity"] + 10 * season_factor + humidity_random))
            
            forecast_data.append({
                "date": date,
                "location": location,
                "temperature_C": round(temp, 1),
                "rainfall_mm": round(rainfall, 0),
                "humidity_pct": round(humidity, 0),
                "confidence": round(max(20, 100 - i * 20), 0)  # Confidence decreases with time
            })
        
        return pd.DataFrame(forecast_data)
    
    def calculate_yield_impact(self, crop, location, planting_date):
        """
        Calculate the expected impact of weather on crop yield
        
        Parameters:
        - crop: Crop type
        - location: Growing location
        - planting_date: When the crop will be planted
        
        Returns:
        - Dictionary with yield impact factors and explanation
        """
        if crop not in self.crop_weather_sensitivity:
            logging.warning(f"Unknown crop: {crop}. Cannot calculate yield impact.")
            return {
                "impact_factor": 1.0,
                "explanation": "No weather impact data available for this crop."
            }
            
        if location not in self.weather_stations:
            logging.warning(f"Unknown location: {location}. Using default weather patterns.")
            location = next(iter(self.weather_stations))
        
        # Get forecast for growing season (assume 4 months)
        forecast = self.get_weather_forecast(location, 4)
        
        # Calculate growing season based on planting date
        if isinstance(planting_date, str):
            planting_date = datetime.datetime.strptime(planting_date, "%Y-%m-%d")
        
        # Get optimal conditions for the crop
        optimal = self.crop_optimal_conditions[crop]
        sensitivity = self.crop_weather_sensitivity[crop]
        
        # Calculate average conditions during growing season
        avg_temp = forecast["temperature_C"].mean()
        avg_rainfall = forecast["rainfall_mm"].mean() * 4  # Total for the season
        avg_humidity = forecast["humidity_pct"].mean()
        
        # Calculate how far conditions are from optimal (0 = optimal, negative = below, positive = above)
        temp_deviation = 0
        if avg_temp < optimal["temp"][0]:
            temp_deviation = (avg_temp - optimal["temp"][0]) / optimal["temp"][0]
        elif avg_temp > optimal["temp"][1]:
            temp_deviation = (avg_temp - optimal["temp"][1]) / optimal["temp"][1]
            
        rainfall_deviation = 0
        if avg_rainfall < optimal["rainfall"][0]:
            rainfall_deviation = (avg_rainfall - optimal["rainfall"][0]) / optimal["rainfall"][0]
        elif avg_rainfall > optimal["rainfall"][1]:
            rainfall_deviation = (avg_rainfall - optimal["rainfall"][1]) / optimal["rainfall"][1]
            
        humidity_deviation = 0
        if avg_humidity < optimal["humidity"][0]:
            humidity_deviation = (avg_humidity - optimal["humidity"][0]) / optimal["humidity"][0]
        elif avg_humidity > optimal["humidity"][1]:
            humidity_deviation = (avg_humidity - optimal["humidity"][1]) / optimal["humidity"][1]
        
        # Calculate impact factors (1.0 = no impact, <1.0 = negative impact, >1.0 = positive impact)
        temp_impact = 1.0 - abs(temp_deviation) * sensitivity["temp"]
        rainfall_impact = 1.0 - abs(rainfall_deviation) * sensitivity["rainfall"]
        humidity_impact = 1.0 - abs(humidity_deviation) * sensitivity["humidity"]
        
        # Calculate overall impact as weighted average
        overall_impact = (temp_impact + rainfall_impact + humidity_impact) / 3
        # Add a small random factor for natural variation
        overall_impact = overall_impact * np.random.uniform(0.95, 1.05)
        overall_impact = max(0.5, min(1.5, overall_impact))  # Cap between 50% and 150%
        
        # Prepare explanation
        explanation = []
        if temp_deviation < -0.1:
            explanation.append(f"Temperature is expected to be colder than optimal ({avg_temp:.1f}°C)")
        elif temp_deviation > 0.1:
            explanation.append(f"Temperature is expected to be warmer than optimal ({avg_temp:.1f}°C)")
            
        if rainfall_deviation < -0.1:
            explanation.append(f"Rainfall is expected to be lower than optimal ({avg_rainfall:.0f}mm)")
        elif rainfall_deviation > 0.1:
            explanation.append(f"Rainfall is expected to be higher than optimal ({avg_rainfall:.0f}mm)")
            
        if humidity_deviation < -0.1:
            explanation.append(f"Humidity is expected to be lower than optimal ({avg_humidity:.0f}%)")
        elif humidity_deviation > 0.1:
            explanation.append(f"Humidity is expected to be higher than optimal ({avg_humidity:.0f}%)")
            
        if not explanation:
            explanation.append("Weather conditions are near optimal for this crop")
            
        impact_text = "reduced" if overall_impact < 0.95 else "increased" if overall_impact > 1.05 else "normal"
        
        return {
            "impact_factor": round(overall_impact, 2),
            "explanation": ". ".join(explanation),
            "forecast_summary": f"Expected {impact_text} yield based on {location} weather forecast."
        } 