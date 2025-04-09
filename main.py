from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

# Initialize agents
advisor = FarmerAdvisor("FarmerAdvisor")
researcher = MarketResearcher("MarketResearcher")

# Simulate message passing
advisor.send_message(researcher, "Suggest profitable crop based on current market trends")
researcher.send_message(advisor, "Crop recommendation: Maize based on demand and pricing")
