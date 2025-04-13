# """
# Phase 5 Test Suite for Farm Assistant
# Comprehensive testing including integration tests, performance benchmarks, and sample farm scenarios
# """

# import logging
# import json
# import time
# from pathlib import Path
# from agents.decision_engine import DecisionEngine
# from database.db_manager import DatabaseManager  # Adjust import based on your actual database module
# from utils.logger import setup_logger  # Adjust import based on your actual logger setup

# # Set up logging
# logger = setup_logger('phase5_tests', 'logs/phase5_tests.log')

# class FarmTestSuite:
#     def __init__(self):
#         self.decision_engine = DecisionEngine()
#         self.db_manager = DatabaseManager()  # Adjust based on your actual database initialization
        
#     def test_small_farm(self):
#         """Test case for a small farm (1-2 crops)"""
#         logger.info("Running small farm test scenario")
#         farm_data = {
#             "name": "Small Test Farm",
#             "size": 2.5,  # hectares
#             "location": {"latitude": 45.5, "longitude": -122.6},
#             "soil_conditions": {
#                 "pH": 6.8,
#                 "moisture": 0.65,
#                 "soil_type": "loam"
#             },
#             "crops": ["tomatoes", "lettuce"]
#         }
        
#         start_time = time.time()
#         recommendations = self.decision_engine.get_comprehensive_recommendation(farm_data)
#         execution_time = time.time() - start_time
        
#         logger.info(f"Small farm test completed in {execution_time:.2f} seconds")
#         return recommendations, execution_time

#     def test_medium_farm(self):
#         """Test case for a medium farm (5-10 crops)"""
#         logger.info("Running medium farm test scenario")
#         farm_data = {
#             "name": "Medium Test Farm",
#             "size": 20.0,  # hectares
#             "location": {"latitude": 45.5, "longitude": -122.6},
#             "soil_conditions": {
#                 "pH": 7.0,
#                 "moisture": 0.60,
#                 "soil_type": "clay loam"
#             },
#             "crops": ["corn", "soybeans", "wheat", "potatoes", "carrots"]
#         }
        
#         start_time = time.time()
#         recommendations = self.decision_engine.get_comprehensive_recommendation(farm_data)
#         execution_time = time.time() - start_time
        
#         logger.info(f"Medium farm test completed in {execution_time:.2f} seconds")
#         return recommendations, execution_time

#     def test_large_farm(self):
#         """Test case for a large farm (10+ crops)"""
#         logger.info("Running large farm test scenario")
#         farm_data = {
#             "name": "Large Test Farm",
#             "size": 100.0,  # hectares
#             "location": {"latitude": 45.5, "longitude": -122.6},
#             "soil_conditions": {
#                 "pH": 6.5,
#                 "moisture": 0.70,
#                 "soil_type": "silt loam"
#             },
#             "crops": [
#                 "corn", "soybeans", "wheat", "barley", "oats",
#                 "potatoes", "sugar beets", "alfalfa", "clover", "peas"
#             ]
#         }
        
#         start_time = time.time()
#         recommendations = self.decision_engine.get_comprehensive_recommendation(farm_data)
#         execution_time = time.time() - start_time
        
#         logger.info(f"Large farm test completed in {execution_time:.2f} seconds")
#         return recommendations, execution_time

#     def run_performance_tests(self):
#         """Run performance benchmarks"""
#         logger.info("Starting performance tests")
#         results = {
#             "small_farm": self.test_small_farm(),
#             "medium_farm": self.test_medium_farm(),
#             "large_farm": self.test_large_farm()
#         }
#         return results

# def main():
#     print("\n" + "="*80)
#     print("🌾 FARM ASSISTANT - PHASE 5 COMPREHENSIVE TESTS")
#     print("="*80 + "\n")
    
#     test_suite = FarmTestSuite()
    
#     try:
#         results = test_suite.run_performance_tests()
        
#         print("\nTest Results Summary:")
#         print("-" * 40)
        
#         for farm_type, (recommendations, execution_time) in results.items():
#             print(f"\n{farm_type.replace('_', ' ').title()}:")
#             print(f"Execution Time: {execution_time:.2f} seconds")
#             print(f"Number of Recommendations: {len(recommendations.get('recommendations', []))}")
#             print("-" * 40)
        
#         print("\n✅ All tests completed successfully!")
        
#     except Exception as e:
#         logger.error(f"Error during testing: {str(e)}")
#         print(f"\n❌ Error during testing: {str(e)}")
    
#     print("\n" + "="*80)

# if __name__ == "__main__":
#     main()
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
