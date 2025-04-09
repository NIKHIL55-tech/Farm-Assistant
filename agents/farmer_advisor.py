from agents.base_agent import BaseAgent
import logging
import re
from utils.db_utils import get_farm_data, get_crop_recommendations

class FarmerAdvisor(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.info(f"Initializing {name} agent")
        # Load farm data on initialization
        self.farm_data = get_farm_data()
        logging.info(f"Loaded {len(self.farm_data)} farm records")
        
    def process_message(self, sender, message):
        logging.info(f"{self.name} processing message: {message}")
        
        if "recommend" in message.lower() or "suggest" in message.lower():
            return self.generate_recommendation(message)
        elif "analyze" in message.lower() or "analyze farm" in message.lower():
            return self.analyze_farm_data()
        else:
            response = f"[{self.name}] I can provide farming recommendations based on soil and climate conditions."
            print(response)
            return response
    
    def analyze_farm_data(self):
        """Analyze farm data for patterns and insights"""
        # Calculate average yield by crop type
        crop_yield = self.farm_data.groupby('Crop_Type')['Crop_Yield_ton'].mean().sort_values(ascending=False)
        top_crops = crop_yield.head(3).index.tolist()
        
        # Calculate average sustainability score
        avg_sustainability = self.farm_data['Sustainability_Score'].mean()
        
        response = f"[{self.name}] Farm Analysis: Top performing crops are {', '.join(top_crops)}. "
        response += f"Average sustainability score across farms: {avg_sustainability:.2f}/10."
        print(response)
        return response
    
    def generate_recommendation(self, message):
        """Generate crop recommendations based on conditions"""
        # Default values (could be extracted from message using NLP in a more advanced version)
        soil_ph = 6.5  # Neutral soil
        rainfall = 800  # mm
        temperature = 25  # Celsius
        
        # Extract farm conditions from message if provided
        message_lower = message.lower()
        if "soil" in message_lower and "ph" in message_lower:
            # Use regex to extract numeric value after "ph" or "pH"
            ph_matches = re.findall(r'ph\s*(\d+\.?\d*)', message_lower)
            if ph_matches:
                try:
                    soil_ph = float(ph_matches[0])
                    logging.info(f"Extracted soil pH: {soil_ph} from message: {message}")
                except ValueError:
                    logging.warning(f"Failed to parse pH value from: {ph_matches[0]}")
        
        # Get soil type description based on pH
        soil_type = "neutral"
        if soil_ph < 6.0:
            soil_type = "acidic"
        elif soil_ph > 7.5:
            soil_type = "alkaline"
        elif soil_ph > 7.0:
            soil_type = "slightly alkaline"
        elif soil_ph < 6.5:
            soil_type = "slightly acidic"
        
        # Get crop recommendations based on soil pH
        recommendations = get_crop_recommendations(soil_ph, rainfall, temperature)
        
        if not recommendations.empty and len(recommendations) > 0:
            # Get top 3 recommendations
            top_crops = recommendations.head(3)['Crop_Type'].tolist()
            
            response = f"[{self.name}] Based on soil pH {soil_ph} ({soil_type} soil), "
            response += f"I recommend: {', '.join(top_crops)}."
            
            # Add extra information based on soil type
            if soil_ph < 6.0:
                response += " For acidic soils, consider applying lime to raise pH if needed for certain crops."
            elif soil_ph > 7.5:
                response += " For alkaline soils, adding organic matter can help manage pH for sensitive crops."
        else:
            # Fallback to general recommendations
            crop_yield = self.farm_data.groupby('Crop_Type')['Crop_Yield_ton'].mean().sort_values(ascending=False)
            top_crops = crop_yield.head(3).index.tolist()
            response = f"[{self.name}] For {soil_type} soil (pH {soil_ph}), based on historical yield data, "
            response += f"I recommend: {', '.join(top_crops)}."
        
        print(response)
        return response
