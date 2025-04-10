from core.decision_engine import DecisionEngine
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

def test_sustainability_score():
    agents = [FarmerAdvisor(name="FarmerAdvisor"), MarketResearcher(name="MarketResearcher")]
    engine = DecisionEngine(agents)

    message = {"query": "Recommend crops for pH 6.2"}
    result = engine.run(message)

    assert isinstance(result, dict)
    assert "recommendation" in result
    assert isinstance(result["recommendation"], list)
