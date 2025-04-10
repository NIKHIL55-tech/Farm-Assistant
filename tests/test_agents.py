# import pytest
# from agents.farmer_advisor import FarmerAdvisor
# from agents.market_researcher import MarketResearcher

# # Test 1: Basic instantiation of FarmerAdvisor
# def test_farmer_advisor_initialization():
#     advisor = FarmerAdvisor(name="FarmerAdvisor")
#     assert advisor.name == "FarmerAdvisor"

# # Test 2: Basic instantiation of MarketResearcher
# def test_market_researcher_initialization():
#     researcher = MarketResearcher(name="MarketResearcher")
#     assert researcher.name == "MarketResearcher"

# # Test 3: Check FarmerAdvisor response to a query
# def test_farmer_advisor_response():
#     advisor = FarmerAdvisor(name="FarmerAdvisor")
#     message = {"type": "crop_advice", "area": "Warangal", "season": "Kharif"}
#     response = advisor.run(message)
#     assert isinstance(response, str)
#     assert "suggest" in response.lower() or "recommend" in response.lower()

# # Test 4: Check MarketResearcher response to a query
# def test_market_researcher_response():
#     researcher = MarketResearcher(name="MarketResearcher")
#     message = {"type": "market_prices", "crop": "Rice"}
#     response = researcher.run(message)
#     assert isinstance(response, str)
#     assert "price" in response.lower() or "market" in response.lower()

# # Test 5: Simulate inter-agent communication
# def test_inter_agent_message_passing():
#     advisor = FarmerAdvisor(name="FarmerAdvisor")
#     researcher = MarketResearcher(name="MarketResearcher")

#     # Advisor sends a message to researcher
#     message = {"type": "market_prices", "crop": "Maize"}
#     response = researcher.run(message)

#     # Make sure the response is meaningful
#     assert isinstance(response, str)
#     assert any(keyword in response.lower() for keyword in ["price", "market", "data"])


from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

def test_farmer_advisor_response():
    advisor = FarmerAdvisor(name="FarmerAdvisor")
    message = {"type": "crop_advice", "area": "Warangal", "season": "Kharif"}
    response = advisor.run(message)

    assert isinstance(response, dict)
    assert "response" in response
    assert isinstance(response["response"], str)

def test_market_researcher_response():
    researcher = MarketResearcher(name="MarketResearcher")
    message = {"type": "market_prices", "crop": "Rice"}
    response = researcher.run(message)

    assert isinstance(response, dict)
    assert "response" in response
    assert isinstance(response["response"], str)

def test_inter_agent_message_passing():
    advisor = FarmerAdvisor(name="FarmerAdvisor")
    researcher = MarketResearcher(name="MarketResearcher")

    message = {"type": "market_prices", "crop": "Maize"}
    response = researcher.run(message)

    assert isinstance(response, dict)
    assert "response" in response
    assert isinstance(response["response"], str)
