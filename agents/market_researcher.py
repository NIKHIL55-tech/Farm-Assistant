from agents.base_agent import BaseAgent
import logging
import pandas as pd
import numpy as np
from utils.db_utils import get_market_data, get_market_trends, query_to_dataframe

class MarketResearcher(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.info(f"Initializing {name} agent")
        self.market_data = get_market_data()
        logging.info(f"Loaded {len(self.market_data)} market records")

    def run(self, message):
        if isinstance(message, dict):
            query = message.get("query", "")
        else:
            query = str(message)
        return self.process_message(self.name, query)

    def process_message(self, sender, message_text):
        logging.info(f"{self.name} processing message: {message_text}")

        if "market" in message_text.lower() and "trend" in message_text.lower():
            return self.analyze_market_trends()
        elif "profitable" in message_text.lower() or "crop" in message_text.lower():
            return self.recommend_profitable_crops()
        elif "price" in message_text.lower():
            for crop in self.get_available_crops():
                if crop.lower() in message_text.lower():
                    return self.get_price_forecast(crop)
            return self.default_response()
        else:
            return self.default_response()

    def default_response(self):
        return {
            "agent": self.name,
            "type": "info",
            "response": "I can analyze market trends, recommend profitable crops, and forecast prices."
        }

    def get_available_crops(self):
        return self.market_data['Product'].unique().tolist()

    def analyze_market_trends(self):
        trends = get_market_trends()
        top_products = trends.head(3)['Product'].tolist()

        opportunity_query = """
        SELECT Product, AVG(Demand_Index) as Avg_Demand, AVG(Supply_Index) as Avg_Supply,
               (AVG(Demand_Index) - AVG(Supply_Index)) as Opportunity_Score
        FROM markets
        GROUP BY Product
        HAVING Avg_Demand > Avg_Supply
        ORDER BY Opportunity_Score DESC
        LIMIT 3
        """
        opportunities = query_to_dataframe(opportunity_query)
        opportunity_products = opportunities['Product'].tolist() if not opportunities.empty else []

        response = f"[{self.name}] Market Trend Analysis: Top products by price×demand: {', '.join(top_products)}. "
        if opportunity_products:
            response += f"Opportunity crops (high demand, low supply): {', '.join(opportunity_products)}."

        return {
            "agent": self.name,
            "type": "market_trend",
            "response": response,
            "top_products": top_products,
            "opportunities": opportunity_products
        }

    def recommend_profitable_crops(self):
        df = self.market_data.copy()
        df['Profitability'] = (df['Market_Price_per_ton'] * df['Demand_Index']) / np.maximum(df['Supply_Index'], 0.1)
        profitability = df.groupby('Product')['Profitability'].mean().sort_values(ascending=False)
        top_profitable = profitability.head(3).index.tolist()

        response = f"[{self.name}] Most profitable crops based on current market: {', '.join(top_profitable)}."
        return {
            "agent": self.name,
            "type": "profitable_crops",
            "recommended_crops": top_profitable,
            "response": response
        }

    def get_price_forecast(self, crop):
        crop_data = self.market_data[self.market_data['Product'] == crop]

        if crop_data.empty:
            return {
                "agent": self.name,
                "type": "price_forecast",
                "crop": crop,
                "response": f"[{self.name}] No market data available for {crop}."
            }

        avg_price = crop_data['Market_Price_per_ton'].mean()
        min_price = crop_data['Market_Price_per_ton'].min()
        max_price = crop_data['Market_Price_per_ton'].max()
        demand = crop_data['Demand_Index'].mean()
        supply = crop_data['Supply_Index'].mean()

        price_trend = "rising" if demand > supply else "stable or falling"

        if demand > supply * 1.2:
            market_condition = "high demand with limited supply"
            outlook = "very favorable"
        elif demand > supply:
            market_condition = "demand exceeds supply"
            outlook = "favorable"
        elif supply > demand * 1.2:
            market_condition = "oversupplied market"
            outlook = "challenging"
        else:
            market_condition = "balanced market"
            outlook = "stable"

        response = (
            f"[{self.name}] {crop} price forecast:\n"
            f"  • Current average price: ${avg_price:.2f}/ton (range: ${min_price:.2f}-${max_price:.2f})\n"
            f"  • Price trend: {price_trend}\n"
            f"  • Market condition: {market_condition}\n"
            f"  • Outlook: {outlook}"
        )

        return {
            "agent": self.name,
            "type": "price_forecast",
            "crop": crop,
            "response": response,
            "details": {
                "avg_price": avg_price,
                "min_price": min_price,
                "max_price": max_price,
                "trend": price_trend,
                "market_condition": market_condition,
                "outlook": outlook
            }
        }
