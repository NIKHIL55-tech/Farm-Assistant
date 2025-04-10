import pandas as pd
import re
from core.sustainability import calculate_sustainability_score

class DecisionEngine:
    def __init__(self, agents):
        self.agents = agents
        self.data = pd.read_csv("data/farmer_advisor_dataset.csv")

    def run(self, message):
        query = message.get("query", "").lower()

        if "ph" in query:
            match = re.search(r'pH\s*([0-9.]+)', query, re.IGNORECASE)
            if match:
                try:
                    target_ph = float(match.group(1))
                    return self._recommend_by_ph(target_ph)
                except ValueError:
                    return {"error": "Invalid pH value provided."}
            return {"response": "No valid pH value found in query."}

        return {"response": "Query not understood."}

    def _recommend_by_ph(self, target_ph):
        # Filter crops with similar pH range (±0.5)
        subset = self.data[
            (self.data["Soil_pH"] >= target_ph - 0.5) &
            (self.data["Soil_pH"] <= target_ph + 0.5)
        ]

        if subset.empty:
            return {"response": "No valid recommendations found."}

        # Calculate sustainability scores
        subset["Sustainability_Score"] = subset.apply(calculate_sustainability_score, axis=1)
        top_crops = subset.sort_values(by="Sustainability_Score", ascending=False).head(3)

        return {
            "recommendation": top_crops[["Crop_Type", "Sustainability_Score"]].to_dict(orient="records")
        }
