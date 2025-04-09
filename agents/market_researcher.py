from agents.base_agent import BaseAgent
import logging
import pandas as pd
import numpy as np
from utils.db_utils import get_market_data, get_market_trends, query_to_dataframe

class MarketResearcher(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.info(f"Initializing {name} agent")
        # Load market data on initialization
        self.market_data = get_market_data()
        logging.info(f"Loaded {len(self.market_data)} market records")
        
    def process_message(self, sender, message):
        logging.info(f"{self.name} processing message: {message}")
        
        if "market" in message.lower() and "trend" in message.lower():
            return self.analyze_market_trends()
        elif "profitable" in message.lower() or "crop" in message.lower():
            return self.recommend_profitable_crops()
        elif "price" in message.lower() and any(crop in message.lower() for crop in self.get_available_crops()):
            # Extract crop name from message
            for crop in self.get_available_crops():
                if crop.lower() in message.lower():
                    return self.get_price_forecast(crop)
            return self.default_response()
        else:
            return self.default_response()
    
    def default_response(self):
        """Default response when no specific query is detected"""
        response = f"[{self.name}] I can analyze market trends, recommend profitable crops, and forecast prices."
        print(response)
        return response
    
    def get_available_crops(self):
        """Get list of crops available in market data"""
        return self.market_data['Product'].unique().tolist()
    
    def analyze_market_trends(self):
        """Analyze current market trends"""
        # Get trending data
        trends = get_market_trends()
        
        # Top 3 trending products
        top_products = trends.head(3)['Product'].tolist()
        
        # Products with high demand but low supply (opportunity)
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
        
        print(response)
        return response
    
    def recommend_profitable_crops(self):
        """Recommend most profitable crops based on current market data"""
        # Calculate profitability score: price * demand / supply
        df = self.market_data.copy()
        df['Profitability'] = (df['Market_Price_per_ton'] * df['Demand_Index']) / np.maximum(df['Supply_Index'], 0.1)
        
        # Group by product and get average profitability
        profitability = df.groupby('Product')['Profitability'].mean().sort_values(ascending=False)
        top_profitable = profitability.head(3).index.tolist()
        
        response = f"[{self.name}] Most profitable crops based on current market: {', '.join(top_profitable)}."
        print(response)
        return response
    
    def get_price_forecast(self, crop):
        """Get price forecast for a specific crop"""
        crop_data = self.market_data[self.market_data['Product'] == crop]
        
        if crop_data.empty:
            response = f"[{self.name}] No market data available for {crop}."
        else:
            # Calculate price metrics
            avg_price = crop_data['Market_Price_per_ton'].mean()
            min_price = crop_data['Market_Price_per_ton'].min()
            max_price = crop_data['Market_Price_per_ton'].max()
            demand = crop_data['Demand_Index'].mean()
            supply = crop_data['Supply_Index'].mean()
            
            # Determine price trend and market conditions
            price_trend = "rising" if demand > supply else "stable or falling"
            
            # Market condition analysis
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
            
            # Generate detailed response
            response = f"[{self.name}] {crop} price forecast: \n"
            response += f"  • Current average price: ${avg_price:.2f}/ton (range: ${min_price:.2f}-${max_price:.2f}) \n"
            response += f"  • Price trend: {price_trend} \n"
            response += f"  • Market condition: {market_condition} \n"
            response += f"  • Outlook: {outlook}"
        
        print(response)
        return response
