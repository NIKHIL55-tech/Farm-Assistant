# from agents.farmer_advisor import FarmerAdvisor
# from agents.market_researcher import MarketResearcher

# # Initialize agents
# advisor = FarmerAdvisor("FarmerAdvisor")
# researcher = MarketResearcher("MarketResearcher")

# # Simulate message passing
# advisor.send_message(researcher, "Suggest profitable crop based on current market trends")
# researcher.send_message(advisor, "Crop recommendation: Maize based on demand and pricing")


# main.py
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from core.coordinator import Coordinator
from core.decision_engine import DecisionEngine

advisor = FarmerAdvisor(name="FarmerAdvisor")
researcher = MarketResearcher(name="MarketResearcher")

coordinator = Coordinator([advisor, researcher], weights={"economic": 0.6, "environmental": 0.4})
engine = DecisionEngine()

msg = {"type": "crop_advice", "area": "Karimnagar", "season": "Kharif"}
recommendations = coordinator.collect_recommendations(msg)
combined = coordinator.resolve_conflicts(recommendations)
score = engine.compute_sustainability_score(combined)
final = engine.aggregate_decisions(combined, score)

print("Final Recommendation:", final)

