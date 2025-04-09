"""
Phase 2 Test Script for Sustainable Agriculture Multi-Agentic AI
This script demonstrates the enhanced functionality of the Farmer Advisor
and Market Researcher agents after Phase 2 implementation.
"""

import logging
import time
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

# Configure logging to console for better visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/system.log"),
        logging.StreamHandler()
    ]
)

def main():
    print("\n" + "="*80)
    print("🌾 AGRICULTURAL INTELLIGENCE NETWORK - PHASE 2 TEST")
    print("="*80 + "\n")
    
    # Initialize agents
    advisor = FarmerAdvisor("FarmerAdvisor")
    researcher = MarketResearcher("MarketResearcher")
    
    print("\n📊 TESTING INDEPENDENT AGENT CAPABILITIES\n")
    
    # Test FarmerAdvisor capabilities
    print("\n🌱 FARMER ADVISOR ANALYSIS")
    print("-"*50)
    advisor.analyze_farm_data()
    time.sleep(1)
    
    # Test crop recommendations with different soil conditions
    print("\n🌱 FARMER ADVISOR RECOMMENDATIONS")
    print("-"*50)
    advisor.process_message(None, "Recommend crops for soil pH 6.5")
    time.sleep(1)
    advisor.process_message(None, "Recommend crops for soil pH 7.2")
    time.sleep(1)
    
    # Test MarketResearcher capabilities
    print("\n💹 MARKET RESEARCHER ANALYSIS")
    print("-"*50)
    researcher.analyze_market_trends()
    time.sleep(1)
    
    # Test profitability recommendations
    print("\n💹 MARKET RESEARCHER RECOMMENDATIONS")
    print("-"*50)
    researcher.recommend_profitable_crops()
    time.sleep(1)
    
    print("\n🤝 TESTING AGENT INTERACTION WORKFLOW\n")
    print("-"*50)
    
    # Simulate a more realistic workflow between agents
    print("\n📋 SCENARIO 1: Farmer asking for sustainable and profitable crop advice\n")
    
    # Step 1: Farmer consults the advisor
    print("Step 1: Farmer consults advisor about crop options")
    farm_request = "I have sandy loam soil with pH 6.8. What crops should I consider?"
    print(f"Farmer to Advisor: {farm_request}")
    advisor_response = advisor.process_message(None, farm_request)
    time.sleep(1)
    
    # Step 2: Advisor consults market researcher for profitability check
    print("\nStep 2: Advisor consults market researcher about crop profitability")
    market_request = "Which of these crops have the best market outlook: Corn, Rice, Soybean?"
    print(f"Advisor to Researcher: {market_request}")
    advisor.send_message(researcher, market_request)
    time.sleep(1)
    
    # Step 3: Final recommendation back to farmer
    print("\nStep 3: Advisor provides final recommendation incorporating market data")
    final_recommendation = "Based on your soil conditions and current market trends, Rice offers the best combination of yield potential and profitability."
    print(f"Advisor to Farmer: {final_recommendation}")
    
    # New test scenario for price forecasting
    print("\n\n📋 SCENARIO 2: Price forecasting for crop planning\n")
    print("-"*50)
    
    # Step 1: Farmer has narrowed down choices and wants price information
    print("Step 1: Farmer requests price forecasts for potential crops")
    farmer_query = "I'm considering planting Rice, Wheat, or Corn. What are the price forecasts for these crops?"
    print(f"Farmer to Researcher: {farmer_query}")
    time.sleep(1)
    
    # Step 2: Market researcher provides price forecasts
    print("\nStep 2: Market researcher provides detailed price analysis")
    print("Researcher analyzes Rice prices:")
    researcher.get_price_forecast("Rice")
    time.sleep(1)
    
    print("\nResearcher analyzes Wheat prices:")
    researcher.get_price_forecast("Wheat")
    time.sleep(1)
    
    print("\nResearcher analyzes Corn prices:")
    researcher.get_price_forecast("Corn")
    time.sleep(1)
    
    # Step 3: Farmer makes decision based on combined information
    print("\nStep 3: Farmer makes decision based on price forecasts and advisor recommendations")
    decision = "After reviewing the price forecasts and soil recommendations, I'll plant Rice on 60% of my land and Corn on 40% to balance profitability with risk."
    print(f"Farmer: {decision}")
    
    print("\n" + "="*80)
    print("🎉 PHASE 2 TESTING COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main() 