from typing import Dict, List, Tuple
from .base_agent import BaseAgent
import logging

class Coordinator(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.weights = {
            'economic': 0.4,
            'environmental': 0.4,
            'social': 0.2
        }
        self.sustainability_metrics = {
            'water_usage': 0.3,
            'soil_impact': 0.4,
            'carbon_footprint': 0.3
        }
        
    def aggregate_recommendations(self, farmer_rec: Dict, market_rec: Dict) -> Dict:
        """Aggregate and weight recommendations from different agents."""
        logging.info("Aggregating recommendations from agents...")
        
        combined_score = {}
        for crop in set(farmer_rec.keys()) | set(market_rec.keys()):
            economic_score = market_rec.get(crop, {}).get('score', 0) * self.weights['economic']
            environmental_score = farmer_rec.get(crop, {}).get('score', 0) * self.weights['environmental']
            sustainability_score = self._calculate_sustainability_score(crop)
            
            combined_score[crop] = {
                'total_score': economic_score + environmental_score + sustainability_score,
                'economic_factor': economic_score,
                'environmental_factor': environmental_score,
                'sustainability_factor': sustainability_score
            }
        
        return combined_score
    
    def _calculate_sustainability_score(self, crop: str) -> float:
        """Calculate sustainability score for a crop based on predefined metrics."""
        # Simplified scoring mechanism - in real system would pull from database
        base_metrics = {
            'Rice': {'water_usage': 0.7, 'soil_impact': 0.6, 'carbon_footprint': 0.5},
            'Corn': {'water_usage': 0.5, 'soil_impact': 0.7, 'carbon_footprint': 0.6},
            'Wheat': {'water_usage': 0.4, 'soil_impact': 0.8, 'carbon_footprint': 0.7},
            'Soybean': {'water_usage': 0.3, 'soil_impact': 0.9, 'carbon_footprint': 0.8}
        }
        
        if crop not in base_metrics:
            return 0.5  # Default middle score for unknown crops
            
        score = sum(
            base_metrics[crop][metric] * weight 
            for metric, weight in self.sustainability_metrics.items()
        )
        return score * self.weights['social']
    
    def resolve_conflicts(self, recommendations: Dict) -> List[Tuple[str, float]]:
        """Resolve conflicts and provide final ordered recommendations."""
        sorted_recs = sorted(
            [(crop, data['total_score']) for crop, data in recommendations.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_recs
    
    def process_message(self, sender: BaseAgent, message: str) -> str:
        """Process incoming messages and coordinate responses."""
        logging.info(f"Coordinator received message from {sender}: {message}")
        # Implementation will be expanded based on specific message types
        return "Message received by coordinator" 