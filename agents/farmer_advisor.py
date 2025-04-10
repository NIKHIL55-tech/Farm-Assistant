# agents/farmer_advisor.py

from agents.base_agent import BaseAgent
import logging
import pandas as pd
import re

class FarmerAdvisor(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.info(f"Initializing {name} agent")
        self.farm_data = pd.read_csv("data/farmer_advisor_dataset.csv")
        logging.info(f"Loaded {len(self.farm_data)} farm records")

    def run(self, message):
        if isinstance(message, dict):
            query = message.get("query", "")
            farm_id = message.get("farm_id", None)
        else:
            query = str(message)
            farm_id = None
        return self.process_message(self.name, query, farm_id)

    def process_message(self, sender, message_text, farm_id=None):
        logging.info(f"{self.name} processing message: {message_text}")

        if "recommend" in message_text.lower() or "suggest" in message_text.lower():
            return self.generate_recommendation(message_text, farm_id)
        elif "analyze" in message_text.lower():
            return self.analyze_farm_data()
        else:
            return {
                "agent": self.name,
                "type": "info",
                "response": "I can provide farming recommendations based on soil and climate conditions."
            }

    def analyze_farm_data(self):
        crop_yield = self.farm_data.groupby('Crop_Type')['Crop_Yield_ton'].mean().sort_values(ascending=False)
        top_crops = crop_yield.head(3).index.tolist()
        avg_sustainability = self.farm_data['Sustainability_Score'].mean()

        response = f"[{self.name}] Farm Analysis: Top performing crops are {', '.join(top_crops)}. "
        response += f"Average sustainability score across farms: {avg_sustainability:.2f}/10."
        return {
            "agent": self.name,
            "type": "farm_analysis",
            "response": response,
            "top_crops": top_crops,
            "sustainability_score": avg_sustainability
        }

    def generate_recommendation(self, message_text, farm_id):
        if farm_id is not None and farm_id in self.farm_data['Farm_ID'].values:
            farm_info = self.farm_data[self.farm_data['Farm_ID'] == farm_id].iloc[0]
            soil_ph = farm_info['Soil_pH']
            rainfall = farm_info['Rainfall_mm']
            temperature = farm_info['Temperature_C']
        else:
            return {
                "agent": self.name,
                "type": "error",
                "response": f"Farm_ID {farm_id} not found in dataset. Please check and try again."
            }

        # Determine soil type
        if soil_ph < 6.0:
            soil_type = "acidic"
        elif soil_ph > 7.5:
            soil_type = "alkaline"
        elif soil_ph > 7.0:
            soil_type = "slightly alkaline"
        elif soil_ph < 6.5:
            soil_type = "slightly acidic"
        else:
            soil_type = "neutral"

        # Recommend based on average yield for similar conditions
        filtered = self.farm_data[
            (self.farm_data["Soil_pH"].between(soil_ph - 0.5, soil_ph + 0.5)) &
            (self.farm_data["Rainfall_mm"].between(rainfall - 100, rainfall + 100)) &
            (self.farm_data["Temperature_C"].between(temperature - 2, temperature + 2))
        ]

        if not filtered.empty:
            recommendations = (
                filtered.groupby("Crop_Type")["Crop_Yield_ton"]
                .agg(['mean', 'count'])
                .sort_values(by="mean", ascending=False)
                .head(3)
                .reset_index()
                .rename(columns={'mean': 'Avg_Yield', 'count': 'Sample_Count'})
            )
            top_crops = recommendations["Crop_Type"].tolist()
            detailed = recommendations.to_dict(orient="records")

            response = f"[{self.name}] Based on soil pH {soil_ph} ({soil_type} soil), I recommend: {', '.join(top_crops)}."
        else:
            response = f"[{self.name}] Not enough data to generate a recommendation for Farm_ID {farm_id}."
            top_crops = []
            detailed = []

        return {
            "agent": self.name,
            "type": "recommendation",
            "soil_ph": soil_ph,
            "soil_type": soil_type,
            "recommended_crops": top_crops,
            "detailed": detailed,
            "response": response
        }
