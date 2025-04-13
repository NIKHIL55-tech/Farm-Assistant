import pytest
from core.decision_engine import DecisionEngine
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

@pytest.fixture
def engine():
    agents = [FarmerAdvisor("FarmerAdvisor"), MarketResearcher("MarketResearcher")]
    return DecisionEngine(agents)


# ✅ Sample Farm Test (Ideal Inputs)
def test_sample_farm_ideal(engine):
    message = {"query": "Recommend crops for pH 6.5, moisture 25.0, temperature 30.0, rainfall 300"}
    result = engine.run(message)
    assert "recommendation" in result
    assert isinstance(result["recommendation"], list)
    assert len(result["recommendation"]) > 0


# 🧪 Edge Case: Extremely Low pH (No Results)
def test_edge_case_low_ph(engine):
    message = {"query": "Recommend crops for pH 3.5"}
    result = engine.run(message)
    assert "response" in result
    assert "No valid" in result["response"]


# 🛑 Invalid Input Handling
def test_invalid_ph_input(engine):
    message = {"query": "Recommend crops for pH abc"}
    result = engine.run(message)
    assert "error" in result or "response" in result


# ⚠️ Missing Query Key
def test_missing_query_key(engine):
    message = {}
    result = engine.run(message)
    assert "response" in result
    assert "Query not understood" in result["response"]


# # 🚫 Empty Dataset Scenario (Simulated)
# def test_empty_dataset(monkeypatch):
#     import pandas as pd
#     from core.decision_engine import DecisionEngine

#     # Patch data to be empty
#     monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: pd.DataFrame())

#     agents = [FarmerAdvisor("FA"), MarketResearcher("MR")]
#     engine = DecisionEngine(agents)
#     message = {"query": "Recommend crops for pH 6.2"}

#     result = engine.run(message)
#     assert "response" in result
#     assert "No valid" in result["response"]



