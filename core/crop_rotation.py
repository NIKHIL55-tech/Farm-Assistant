import pandas as pd
import logging

class CropRotationPlanner:
    def __init__(self):
        self.crop_families = {
            "Corn": "Grass",
            "Rice": "Grass",
            "Wheat": "Grass",
            "Soybean": "Legume",
            "Chickpea": "Legume",
            "Cotton": "Mallow",
            "Potato": "Nightshade",
            "Tomato": "Nightshade",
            "Carrot": "Umbellifer",
            "Cabbage": "Brassica",
            "Sunflower": "Aster"
        }
        
        # Rotation compatibility (1: compatible, 0: neutral, -1: avoid)
        self.rotation_compatibility = {
            "Grass": {"Grass": -1, "Legume": 1, "Nightshade": 0, "Brassica": 1, "Umbellifer": 0, "Mallow": 0, "Aster": 0},
            "Legume": {"Grass": 1, "Legume": -1, "Nightshade": 1, "Brassica": 0, "Umbellifer": 0, "Mallow": 0, "Aster": 0},
            "Nightshade": {"Grass": 0, "Legume": 1, "Nightshade": -1, "Brassica": 0, "Umbellifer": 0, "Mallow": 0, "Aster": 0},
            "Brassica": {"Grass": 1, "Legume": 0, "Nightshade": 0, "Brassica": -1, "Umbellifer": 0, "Mallow": 0, "Aster": 0},
            "Umbellifer": {"Grass": 0, "Legume": 0, "Nightshade": 0, "Brassica": 0, "Umbellifer": -1, "Mallow": 0, "Aster": 0},
            "Mallow": {"Grass": 0, "Legume": 0, "Nightshade": 0, "Brassica": 0, "Umbellifer": 0, "Mallow": -1, "Aster": 0},
            "Aster": {"Grass": 0, "Legume": 0, "Nightshade": 0, "Brassica": 0, "Umbellifer": 0, "Mallow": 0, "Aster": -1}
        }
        
        # Soil nutrient impact (N: Nitrogen, P: Phosphorus, K: Potassium)
        self.nutrient_impact = {
            "Grass": {"N": -2, "P": -1, "K": -1},          # Heavy feeders
            "Legume": {"N": 2, "P": -1, "K": -1},          # N fixers
            "Nightshade": {"N": -2, "P": -2, "K": -2},     # Heavy feeders
            "Brassica": {"N": -2, "P": -1, "K": -1},       # Heavy feeders
            "Umbellifer": {"N": -1, "P": -1, "K": -1},     # Medium feeders
            "Mallow": {"N": -2, "P": -1, "K": -1},         # Heavy feeders
            "Aster": {"N": -1, "P": -1, "K": -1}           # Medium feeders
        }
    
    def suggest_rotation(self, current_crop, soil_health=None, years=3):
        """
        Suggest a crop rotation plan based on current crop and soil health
        
        Parameters:
        - current_crop: The crop currently being grown
        - soil_health: Dict with N, P, K levels (optional)
        - years: Number of years to plan rotation for
        
        Returns:
        - List of crop families for rotation
        """
        if current_crop not in self.crop_families:
            logging.warning(f"Unknown crop: {current_crop}. Cannot suggest rotation.")
            return []
            
        current_family = self.crop_families[current_crop]
        rotation_plan = [current_family]
        
        # Build rotation plan based on compatibility and soil needs
        for i in range(years):
            last_family = rotation_plan[-1]
            compatibility_scores = {}
            
            for family, score in self.rotation_compatibility[last_family].items():
                compatibility_scores[family] = score
                
                # Adjust based on soil needs if provided
                if soil_health:
                    nutrient_impact = self.nutrient_impact[family]
                    # Add bonus for families that address soil deficiencies
                    for nutrient, level in soil_health.items():
                        if level < 0 and nutrient_impact.get(nutrient, 0) > 0:
                            compatibility_scores[family] += 1
                        elif level > 0 and nutrient_impact.get(nutrient, 0) < 0:
                            compatibility_scores[family] += 0.5
            
            # Choose the best family for next rotation (excluding current family)
            next_family = max((f for f in compatibility_scores.keys() if f != last_family), 
                            key=lambda f: compatibility_scores[f])
            rotation_plan.append(next_family)
        
        # Remove the first entry (current family) from the plan
        return rotation_plan[1:]
    
    def get_crop_examples(self, family):
        """Get example crops from a given family"""
        return [crop for crop, fam in self.crop_families.items() if fam == family]
    
    def format_rotation_plan(self, current_crop, rotation_plan):
        """Format the rotation plan with crop examples and benefits"""
        if not rotation_plan:
            return "Could not generate a rotation plan for this crop."
            
        current_family = self.crop_families.get(current_crop, "Unknown")
        result = [f"Current crop: {current_crop} (Family: {current_family})"]
        result.append("Recommended rotation plan:")
        
        for i, family in enumerate(rotation_plan):
            examples = self.get_crop_examples(family)
            example_str = ", ".join(examples[:3])
            year = i + 1
            result.append(f"Year {year}: {family} family (e.g., {example_str})")
            
            # Add benefits
            benefits = []
            if family == "Legume":
                benefits.append("fixes nitrogen in soil")
            if self.rotation_compatibility[current_family].get(family, 0) > 0:
                benefits.append("breaks pest/disease cycles")
            
            if benefits:
                result.append(f"  Benefits: {', '.join(benefits)}")
                
        return "\n".join(result) 