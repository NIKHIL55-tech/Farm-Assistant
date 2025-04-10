import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os
import logging

class YieldPredictor:
    def __init__(self, load_pretrained=True):
        self.farm_data = pd.read_csv("data/farmer_advisor_dataset.csv")
        self.models = {}
        self.scalers = {}
        self.important_features = [
            'Soil_pH', 'Rainfall_mm', 'Temperature_C', 'Soil_Moisture',
            'Fertilizer_Usage_kg', 'Pesticide_Usage_kg'
        ]
        self.categorical_features = []
        
        # Setup models directory
        self.models_dir = "models"
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
            
        # Initialize models
        if load_pretrained:
            self._load_or_train_models()
        
    def _preprocess_data(self, data, crop_type, for_training=True):
        """Preprocess data for model training or prediction"""
        # Filter data for specific crop if training
        if for_training:
            crop_data = data[data['Crop_Type'] == crop_type].copy()
            if len(crop_data) < 10:  # Not enough samples
                return None, None
        else:
            crop_data = data.copy()
            
        # One-hot encode categorical features
        for feature in self.categorical_features:
            if feature in crop_data.columns:
                dummies = pd.get_dummies(crop_data[feature], prefix=feature, drop_first=True)
                crop_data = pd.concat([crop_data, dummies], axis=1)
                crop_data.drop(feature, axis=1, inplace=True)
        
        # Select features for model
        available_features = [f for f in self.important_features if f in crop_data.columns]
        dummy_cols = [col for col in crop_data.columns if any(col.startswith(f + '_') for f in self.categorical_features)]
        
        feature_cols = [col for col in available_features if col not in self.categorical_features] + dummy_cols
        
        if for_training:
            X = crop_data[feature_cols]
            y = crop_data['Crop_Yield_ton']
            return X, y
        else:
            X = crop_data[feature_cols]
            return X, feature_cols
            
    def _load_or_train_models(self):
        """Load pretrained models or train new ones if not available"""
        crop_types = self.farm_data['Crop_Type'].unique()
        
        for crop in crop_types:
            model_path = os.path.join(self.models_dir, f"{crop}_yield_model.pkl")
            scaler_path = os.path.join(self.models_dir, f"{crop}_scaler.pkl")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                # Load pretrained model and scaler
                try:
                    with open(model_path, 'rb') as f:
                        self.models[crop] = pickle.load(f)
                    with open(scaler_path, 'rb') as f:
                        self.scalers[crop] = pickle.load(f)
                    logging.info(f"Loaded pretrained model for {crop}")
                except Exception as e:
                    logging.error(f"Error loading model for {crop}: {e}")
                    self._train_model(crop)
            else:
                # Train new model
                self._train_model(crop)
    
    def _train_model(self, crop_type):
        """Train a yield prediction model for a specific crop type"""
        X, y = self._preprocess_data(self.farm_data, crop_type)
        
        if X is None or y is None or len(X) < 10:
            logging.warning(f"Not enough data to train model for {crop_type}")
            return
            
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers[crop_type] = scaler
        
        # Train model (using RandomForest for better accuracy)
        model = RandomForestRegressor(
            n_estimators=100, 
            max_depth=10,
            random_state=42
        )
        model.fit(X_scaled, y)
        self.models[crop_type] = model
        
        # Save model and scaler
        model_path = os.path.join(self.models_dir, f"{crop_type}_yield_model.pkl")
        scaler_path = os.path.join(self.models_dir, f"{crop_type}_scaler.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
            
        logging.info(f"Trained and saved model for {crop_type}")
        
        # Calculate and store feature importances
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        self.feature_importances = feature_importance
            
    def predict_yield(self, crop_type, field_data, weather_impact=1.0):
        """
        Predict yield for a crop based on field data and weather impact
        
        Parameters:
        - crop_type: Type of crop to predict yield for
        - field_data: Dictionary with field characteristics
        - weather_impact: Weather impact factor (default: 1.0 = no impact)
        
        Returns:
        - Dictionary with yield prediction and explanation
        """
        if crop_type not in self.models:
            # Train model if not already available
            self._train_model(crop_type)
            
            # If still not available, not enough data
            if crop_type not in self.models:
                return {
                    "yield_prediction": None,
                    "explanation": f"Insufficient data to make predictions for {crop_type}",
                    "confidence": 0
                }
        
        # Create a mapping from form field names to model feature names
        field_to_feature_mapping = {
            'farm_id': 'Farm_ID',
            'field_size': 'Soil_Moisture',  # Use as proxy for field size
            'soil_ph': 'Soil_pH',
            'rainfall': 'Rainfall_mm',
            'temperature': 'Temperature_C',
            'pesticide_use': 'Pesticide_Usage_kg',
            'fertilizer_use': 'Fertilizer_Usage_kg',
            # URL parameter names (from form submission)
            'Farm_ID': 'Farm_ID',
            'Field_Size_hectare': 'Soil_Moisture',  # Use as proxy for field size
            'Soil_pH': 'Soil_pH', 
            'Rainfall_mm': 'Rainfall_mm',
            'Temperature_C': 'Temperature_C',
            'Pesticide_Use_kg': 'Pesticide_Usage_kg',
            'Fertilizer_Use_kg': 'Fertilizer_Usage_kg',
            # Direct matches
            'Soil_Moisture': 'Soil_Moisture',
            'Pesticide_Usage_kg': 'Pesticide_Usage_kg',
            'Fertilizer_Usage_kg': 'Fertilizer_Usage_kg'
        }
        
        # Normalize field data to match expected feature names
        normalized_data = {}
        for key, value in field_data.items():
            if key in field_to_feature_mapping:
                normalized_data[field_to_feature_mapping[key]] = value
            else:
                # For any keys not in the mapping, try to match case-insensitive
                for feature in self.important_features:
                    if key.lower() == feature.lower() or key.replace('_', '') == feature.replace('_', ''):
                        normalized_data[feature] = value
                        break
                else:
                    # If no match found, keep the original key
                    normalized_data[key] = value
        
        logging.info(f"Normalized data for prediction: {normalized_data}")
                
        # Convert field data to DataFrame
        field_df = pd.DataFrame([normalized_data])
        
        # Get the training features for this crop type
        # We need to recreate the same preprocessing pipeline used for training
        X_train, _ = self._preprocess_data(self.farm_data[self.farm_data['Crop_Type'] == crop_type], crop_type, for_training=True)
        if X_train is None:
            return {
                "yield_prediction": None,
                "explanation": f"Insufficient training data for {crop_type}",
                "confidence": 0
            }
        
        # Process the input data using the same transformation
        # First, handle categorical features
        for feature in self.categorical_features:
            if feature in field_df.columns:
                # Get unique values from training data for this categorical feature
                train_categories = self.farm_data[self.farm_data['Crop_Type'] == crop_type][feature].unique()
                
                # One-hot encode the categorical feature
                for category in train_categories:
                    dummy_name = f"{feature}_{category}"
                    if dummy_name in X_train.columns:
                        field_df[dummy_name] = 1 if field_df[feature].iloc[0] == category else 0
                
                # Drop the original categorical column
                field_df.drop(feature, axis=1, inplace=True)
        
        # Ensure all columns from training exist in prediction data (with same order)
        for col in X_train.columns:
            if col not in field_df.columns:
                field_df[col] = 0  # Default value for missing columns
        
        # Select only the columns that were used during training, in the same order
        X = field_df[X_train.columns]
        
        # Scale the features
        X_scaled = self.scalers[crop_type].transform(X)
        
        # Make prediction
        base_yield = self.models[crop_type].predict(X_scaled)[0]
        
        # Apply weather impact factor
        adjusted_yield = base_yield * weather_impact
        
        # Calculate confidence based on how similar this is to training data
        # Simple method: higher confidence if field data is within typical ranges
        typical_ranges = self.farm_data[self.farm_data['Crop_Type'] == crop_type].describe()
        in_range_count = 0
        feature_comments = []
        
        for feature in [f for f in self.important_features if f not in self.categorical_features]:
            if feature in normalized_data and feature in typical_ranges.columns:
                value = normalized_data[feature]
                low = typical_ranges[feature]['25%']
                high = typical_ranges[feature]['75%']
                
                if low <= value <= high:
                    in_range_count += 1
                elif value < typical_ranges[feature]['min'] or value > typical_ranges[feature]['max']:
                    feature_comments.append(f"{feature} is outside typical range")
        
        num_features = len([f for f in self.important_features if f not in self.categorical_features and f in normalized_data])
        confidence_pct = min(90, round((in_range_count / max(1, num_features)) * 100))
        
        # Generate explanation
        if weather_impact < 0.9:
            weather_effect = "reduced due to unfavorable weather conditions"
        elif weather_impact > 1.1:
            weather_effect = "increased due to favorable weather conditions"
        else:
            weather_effect = "not significantly affected by weather"
            
        explanation = f"Expected yield is {weather_effect}."
        
        if feature_comments:
            explanation += f" Note: {'; '.join(feature_comments)}."
        
        # Format the result
        return {
            "yield_prediction": round(adjusted_yield, 2),
            "base_yield": round(base_yield, 2),
            "weather_impact": round(weather_impact, 2),
            "unit": "tons/hectare",
            "explanation": explanation,
            "confidence": confidence_pct
        }
        
    def get_feature_importance(self, crop_type):
        """Get the importance of different features for yield prediction"""
        if crop_type not in self.models:
            return None
            
        # Use the cached feature importances if available
        if hasattr(self, 'feature_importances'):
            return self.feature_importances
            
        # Otherwise, calculate them
        X, _ = self._preprocess_data(self.farm_data, crop_type)
        
        if X is None:
            return None
            
        importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': self.models[crop_type].feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return importance
        
    def evaluate_management_practices(self, crop_type, field_data):
        """
        Evaluate the effectiveness of different management practices
        
        Parameters:
        - crop_type: Type of crop
        - field_data: Current field data
        
        Returns:
        - Dictionary with recommendations for management practices
        """
        if crop_type not in self.models:
            return None
        
        # Normalize field data - ensure keys match the expected feature names
        normalized_data = {}
        for key, value in field_data.items():
            # Some keys might be capitalized or have slight variations
            for feature in self.important_features:
                if key.lower() == feature.lower() or key.replace('_', '') == feature.replace('_', ''):
                    normalized_data[feature] = value
                    break
            else:
                # If no match found, keep the original key
                normalized_data[key] = value
                
        # Get current values - map from form field names to actual dataset column names
        fertilizer = normalized_data.get('Fertilizer_Usage_kg', 
                     normalized_data.get('Fertilizer_Use_kg', 0))
        
        pesticide = normalized_data.get('Pesticide_Usage_kg', 
                   normalized_data.get('Pesticide_Use_kg', 0))
            
        # Define optimum ranges for each crop
        optimal_ranges = {
            'Rice': {'fertilizer': (80, 120), 'pesticide': (1.5, 2.5)},
            'Wheat': {'fertilizer': (100, 150), 'pesticide': (1.0, 2.0)},
            'Maize': {'fertilizer': (120, 180), 'pesticide': (1.5, 2.5)},
            'Potato': {'fertilizer': (150, 200), 'pesticide': (2.0, 3.0)},
            'Cotton': {'fertilizer': (100, 150), 'pesticide': (2.0, 3.0)},
            # Default values for other crops
            'default': {'fertilizer': (100, 150), 'pesticide': (1.5, 2.5)}
        }
        
        # Get optimal range for this crop
        crop_range = optimal_ranges.get(crop_type, optimal_ranges['default'])
        
        # Generate recommendations
        recommendations = []
        
        # Fertilizer recommendation
        fert_min, fert_max = crop_range['fertilizer']
        if fertilizer < fert_min:
            recommendations.append(f"Consider increasing fertilizer application to {fert_min}-{fert_max} kg/hectare for optimal yield.")
        elif fertilizer > fert_max:
            recommendations.append(f"Consider reducing fertilizer application to {fert_min}-{fert_max} kg/hectare for optimal yield and environmental sustainability.")
        else:
            recommendations.append("Fertilizer application is within optimal range.")
            
        # Pesticide recommendation
        pest_min, pest_max = crop_range['pesticide']
        if pesticide < pest_min:
            recommendations.append(f"Consider increasing pesticide application to {pest_min}-{pest_max} kg/hectare for pest management.")
        elif pesticide > pest_max:
            recommendations.append(f"Consider reducing pesticide application to {pest_min}-{pest_max} kg/hectare for environmental sustainability.")
        else:
            recommendations.append("Pesticide application is within optimal range.")
            
        # Irrigation recommendation
        irrigation_recommendations = {
            'Rice': 'Flood',
            'Wheat': 'Sprinkler',
            'Maize': 'Drip',
            'Potato': 'Sprinkler',
            'Cotton': 'Drip'
        }
        
        recommended_irrigation = irrigation_recommendations.get(crop_type)
        if recommended_irrigation:
            recommendations.append(f"Consider switching to {recommended_irrigation} irrigation for optimal water use efficiency for {crop_type}.")
            
        # Format recommendations for template
        formatted_recommendations = []
        for i, rec in enumerate(recommendations):
            # Calculate a simulated impact value
            if "increasing" in rec:
                impact = 0.5
            elif "reducing" in rec:
                impact = -0.2
            elif "switching" in rec:
                impact = 0.3
            else:
                impact = 0.0
                
            formatted_recommendations.append({
                "practice": f"Practice {i+1}",
                "recommendation": rec,
                "impact": impact
            })
            
        # Return results
        return {
            "recommendations": formatted_recommendations,
            "optimal_ranges": {
                "fertilizer": f"{fert_min}-{fert_max} kg/hectare",
                "pesticide": f"{pest_min}-{pest_max} kg/hectare",
                "recommended_irrigation": recommended_irrigation or "Not specified"
            }
        } 