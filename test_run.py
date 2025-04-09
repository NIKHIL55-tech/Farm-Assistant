from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

# Create agents
advisor = FarmerAdvisor("FarmerAdvisor")
researcher = MarketResearcher("MarketResearcher")

# Message passing test
researcher.send_message(advisor, "Suggest crops for 2.5 hectares black soil.")
advisor.send_message(researcher, "What are current price trends?")
