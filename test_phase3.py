"""
Phase 3 Test Script for Sustainable Agriculture Multi-Agentic AI
This script demonstrates the enhanced coordination and decision-making capabilities
after Phase 3 implementation.
"""

import logging
import json
from agents.decision_engine import DecisionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/phase3.log"),
        logging.StreamHandler()
    ]
)

def print_recommendations(data: dict, title: str = ""):
    """Helper function to print recommendations in a formatted way."""
    print(f"\n{title}")
    print("-" * 80)
    
    if 'recommendations' in data:
        print("\n🌾 Top Crop Recommendations:")
        for crop, score in data['recommendations']:
            print(f"- {crop}: {score:.2f}")
    
    if 'sustainability_metrics' in data:
        metrics = data['sustainability_metrics']
        print("\n🌿 Sustainability Metrics:")
        print(f"Overall Sustainability Score: {metrics['overall_sustainability_score']:.2f}")
        print(f"Environmental Impact Score: {metrics['environmental_impact_score']:.2f}")
        
        if metrics['recommendations']:
            print("\n📋 Sustainability Recommendations:")
            for rec in metrics['recommendations']:
                print(f"- {rec}")

def main():
    print("\n" + "="*80)
    print("🌾 AGRICULTURAL INTELLIGENCE NETWORK - PHASE 3 TEST")
    print("="*80 + "\n")
    
    # Initialize the decision engine
    engine = DecisionEngine()
    
    # Test Case 1: Basic Recommendation
    print("\n📊 TEST CASE 1: BASIC RECOMMENDATION")
    print("-"*80)
    
    soil_conditions = {
        'pH': 6.8,
        'moisture': 0.6,
        'soil_type': 'loam'
    }
    
    print(f"\nAnalyzing soil conditions: {json.dumps(soil_conditions, indent=2)}")
    recommendations = engine.get_comprehensive_recommendation(soil_conditions)
    print_recommendations(recommendations, "COMPREHENSIVE ANALYSIS RESULTS")
    
    # Test Case 2: Scenario Analysis
    print("\n\n📊 TEST CASE 2: SCENARIO ANALYSIS")
    print("-"*80)
    
    scenarios = engine.simulate_scenarios(soil_conditions)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}:")
        print(f"Modified conditions: {json.dumps(scenario['conditions'], indent=2)}")
        print_recommendations(scenario['outcomes'], f"SCENARIO {i} RESULTS")
    
    print("\n" + "="*80)
    print("🎉 PHASE 3 TESTING COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main() 