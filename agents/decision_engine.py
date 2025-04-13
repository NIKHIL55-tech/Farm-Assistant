from typing import Dict, List, Optional
import logging
from .coordinator import Coordinator
from .farmer_advisor import FarmerAdvisor
from .market_researcher import MarketResearcher

class DecisionEngine:
    def __init__(self):
        self.coordinator = Coordinator("MainCoordinator")
        self.farmer_advisor = FarmerAdvisor("FarmAdvisor")
        self.market_researcher = MarketResearcher("MarketResearcher")
        
        logging.info("Decision Engine initialized with all agents")
        
    def get_comprehensive_recommendation(self, soil_conditions: Dict) -> Dict:
        """Generate comprehensive recommendation based on all factors."""
        # Get farm-based recommendations
        farm_recs = self.farmer_advisor.get_crop_recommendations(soil_conditions)
        
        # Get market-based recommendations
        market_recs = self.market_researcher.get_market_recommendations()
        
        # Aggregate recommendations through coordinator
        combined_scores = self.coordinator.aggregate_recommendations(farm_recs, market_recs)
        
        # Get final ordered recommendations
        final_recommendations = self.coordinator.resolve_conflicts(combined_scores)
        
        return {
            'recommendations': final_recommendations,
            'detailed_scores': combined_scores,
            'sustainability_metrics': self._get_sustainability_report(combined_scores)
        }
    
    def _get_sustainability_report(self, scores: Dict) -> Dict:
        """Generate sustainability metrics report."""
        total_environmental_impact = sum(
            data['environmental_factor'] for data in scores.values()
        )
        
        total_sustainability_score = sum(
            data['sustainability_factor'] for data in scores.values()
        )
        
        return {
            'overall_sustainability_score': total_sustainability_score / len(scores) if scores else 0,
            'environmental_impact_score': total_environmental_impact / len(scores) if scores else 0,
            'recommendations': self._generate_sustainability_recommendations(scores)
        }
    
    def _generate_sustainability_recommendations(self, scores: Dict) -> List[str]:
        """Generate specific sustainability recommendations based on scores."""
        recommendations = []
        
        # Analyze scores and generate specific recommendations
        low_sustainability_threshold = 0.4
        for crop, data in scores.items():
            if data['sustainability_factor'] < low_sustainability_threshold:
                recommendations.append(
                    f"Consider alternatives to {crop} for better sustainability scores"
                )
            if data['environmental_factor'] < low_sustainability_threshold:
                recommendations.append(
                    f"Implement sustainable farming practices for {crop} to improve environmental impact"
                )
                
        return recommendations
    
    def simulate_scenarios(self, base_conditions: Dict, num_scenarios: int = 3) -> List[Dict]:
        """Simulate different scenarios for decision making."""
        scenarios = []
        
        # Generate variations of base conditions
        for i in range(num_scenarios):
            modified_conditions = self._modify_conditions(base_conditions, i)
            recommendation = self.get_comprehensive_recommendation(modified_conditions)
            scenarios.append({
                'conditions': modified_conditions,
                'outcomes': recommendation
            })
            
        return scenarios
    
    def _modify_conditions(self, base_conditions: Dict, scenario_index: int) -> Dict:
        """Create variations of conditions for scenario analysis."""
        # Simple modification logic - can be expanded based on needs
        modifications = {
            0: {'pH_adjustment': 0.5, 'moisture_adjustment': 1.1},
            1: {'pH_adjustment': -0.3, 'moisture_adjustment': 0.9},
            2: {'pH_adjustment': 0.2, 'moisture_adjustment': 1.0}
        }
        
        mod = modifications.get(scenario_index, {'pH_adjustment': 0, 'moisture_adjustment': 1.0})
        
        return {
            'pH': base_conditions.get('pH', 7.0) + mod['pH_adjustment'],
            'moisture': base_conditions.get('moisture', 0.5) * mod['moisture_adjustment'],
            'soil_type': base_conditions.get('soil_type', 'loam')
        } 