from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from core.crop_rotation import CropRotationPlanner
from core.weather_integration import WeatherIntegration
from core.yield_prediction import YieldPredictor
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from core.coordinator import Coordinator
from core.decision_engine import DecisionEngine
import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

# Initialize components
farm_data = pd.read_csv("data/farmer_advisor_dataset.csv")
market_data = pd.read_csv("data/market_researcher_dataset.csv")
crop_rotation = CropRotationPlanner()
weather = WeatherIntegration()
yield_predictor = YieldPredictor(load_pretrained=False)  # Don't load pretrained in init to speed startup

# Initialize agents
advisor = FarmerAdvisor(name="FarmerAdvisor")
researcher = MarketResearcher(name="MarketResearcher")
coordinator = Coordinator([advisor, researcher], weights={"economic": 0.6, "environmental": 0.4})
engine = DecisionEngine([advisor, researcher])

# Get available locations from weather integration instead of farm_data
locations = sorted(list(weather.weather_stations.keys()))
crops = sorted(farm_data['Crop_Type'].unique())
soil_types = sorted(farm_data['Soil_Type'].unique()) if 'Soil_Type' in farm_data.columns else ["Clay", "Loam", "Sandy", "Silt"]
irrigation_types = sorted(['Drip', 'Sprinkler', 'Flood', 'Furrow'])

@app.route('/')
def index():
    """Render the main dashboard"""
    # Get basic stats for dashboard
    total_farms = len(farm_data['Farm_ID'].unique())
    avg_yield = farm_data['Crop_Yield_ton'].mean()
    avg_sustainability = farm_data['Sustainability_Score'].mean()
    
    # Get top crops by yield
    top_crops = (
        farm_data.groupby('Crop_Type')['Crop_Yield_ton']
        .mean()
        .sort_values(ascending=False)
        .head(5)
    ).to_dict()
    
    # Get recent market prices - modified to use correct column names
    # Using 'Product' instead of 'Crop_Type' and 'Market_Price_per_ton' instead of 'Price_per_ton'
    recent_prices = (
        market_data
        .sort_values('Market_ID')  # Sort by Market_ID instead of Date
        .drop_duplicates(subset=['Product'])
        .head(5)[['Product', 'Market_Price_per_ton']]
        .set_index('Product')['Market_Price_per_ton']
        .to_dict()
    )
    
    return render_template(
        'index.html',
        total_farms=total_farms,
        avg_yield=round(avg_yield, 2),
        avg_sustainability=round(avg_sustainability, 2),
        top_crops=top_crops,
        recent_prices=recent_prices,
        locations=locations,
        crops=crops
    )

@app.route('/farm-input', methods=['GET', 'POST'])
def farm_input():
    """Handle farm data input form"""
    if request.method == 'POST':
        # Extract form data
        farm_data = {
            'Farm_ID': request.form.get('farm_id', ''),
            'Location': request.form.get('location', ''),
            'Field_Size_hectare': float(request.form.get('field_size', 0)),
            'Soil_pH': float(request.form.get('soil_ph', 0)),
            'Soil_Type': request.form.get('soil_type', ''),
            'Rainfall_mm': float(request.form.get('rainfall', 0)),
            'Temperature_C': float(request.form.get('temperature', 0)),
            'Irrigation_Type': request.form.get('irrigation_type', ''),
            'Pesticide_Use_kg': float(request.form.get('pesticide_use', 0)),
            'Fertilizer_Use_kg': float(request.form.get('fertilizer_use', 0))
        }
        
        # Store in session or temporary database
        # For demo, just redirect to recommendation with parameters
        param_str = '&'.join([f"{k}={v}" for k, v in farm_data.items()])
        return redirect(f"/recommendation?{param_str}")
    
    # GET request - render the input form
    return render_template(
        'farm_input.html',
        locations=locations,
        soil_types=soil_types,
        irrigation_types=irrigation_types
    )

@app.route('/recommendation')
def recommendation():
    """Generate and display recommendations"""
    # Extract farm data from query parameters
    farm_data = {
        'Farm_ID': request.args.get('Farm_ID', ''),
        'Location': request.args.get('Location', ''),
        'Field_Size_hectare': float(request.args.get('Field_Size_hectare', 0)),
        'Soil_pH': float(request.args.get('Soil_pH', 0)),
        'Soil_Type': request.args.get('Soil_Type', ''),
        'Rainfall_mm': float(request.args.get('Rainfall_mm', 0)),
        'Temperature_C': float(request.args.get('Temperature_C', 0)),
        'Irrigation_Type': request.args.get('Irrigation_Type', ''),
        'Pesticide_Use_kg': float(request.args.get('Pesticide_Use_kg', 0)),
        'Fertilizer_Use_kg': float(request.args.get('Fertilizer_Use_kg', 0))
    }
    
    # Get recommendations from agents
    query = f"Recommend crops for soil pH {farm_data['Soil_pH']}"
    agent_recommendations = engine.run({"query": query})
    
    # Get weather forecast for location
    weather_forecast = weather.get_weather_forecast(farm_data['Location'], months_ahead=3)
    
    # For the top 3 recommended crops, get:
    recommended_crops = agent_recommendations.get('recommendation', [])
    crop_details = []
    
    for crop_rec in recommended_crops[:3]:
        crop_type = crop_rec.get('Crop_Type', '')
        
        # 1. Weather impact on yield
        weather_impact = weather.calculate_yield_impact(
            crop_type, 
            farm_data['Location'],
            datetime.datetime.now()
        )
        
        # 2. Yield prediction
        yield_prediction = yield_predictor.predict_yield(
            crop_type,
            farm_data,
            weather_impact.get('impact_factor', 1.0)
        )
        
        # 3. Crop rotation suggestion
        rotation_plan = crop_rotation.suggest_rotation(crop_type)
        rotation_text = crop_rotation.format_rotation_plan(crop_type, rotation_plan)
        
        # 4. Market price forecast
        message = {"query": f"Forecast prices for {crop_type}"}
        price_forecast = researcher.run(message)
        
        # 5. Management practices
        management = yield_predictor.evaluate_management_practices(crop_type, farm_data)
        
        # Collect results
        crop_details.append({
            'crop_type': crop_type,
            'sustainability_score': crop_rec.get('Sustainability_Score', 0),
            'weather_impact': weather_impact,
            'yield_prediction': yield_prediction,
            'rotation_plan': rotation_text,
            'price_forecast': price_forecast,
            'management': management
        })
    
    # Render recommendation template
    return render_template(
        'recommendation.html',
        farm_data=farm_data,
        crop_details=crop_details,
        weather_forecast=weather_forecast.to_dict('records')
    )

@app.route('/charts/price_trends')
def price_trend_chart():
    """Generate price trend chart for crops"""
    selected_crops = request.args.get('crops', '').split(',')
    if not selected_crops or selected_crops[0] == '':
        selected_crops = crops[:3]  # Default to first 3 crops
    
    # Filter data for selected crops and prepare for plotting
    # Using 'Product' instead of 'Crop_Type'
    df = market_data[market_data['Product'].isin(selected_crops)].copy()
    
    # Create a dummy date column based on Market_ID for temporal visualization
    # This is a workaround since our market data doesn't have actual dates
    df['dummy_date'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(df['Market_ID'], unit='D')
    
    # Create the price trend chart
    fig = px.line(
        df, 
        x='dummy_date', 
        y='Market_Price_per_ton', 
        color='Product',
        title='Crop Price Trends',
        labels={'Market_Price_per_ton': 'Price (per ton)', 'dummy_date': 'Date'}
    )
    
    # Convert to JSON for the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/charts/sustainability')
def sustainability_chart():
    """Generate sustainability comparison chart"""
    selected_crops = request.args.get('crops', '').split(',')
    if not selected_crops or selected_crops[0] == '':
        selected_crops = crops[:3]  # Default to first 3 crops
    
    # Calculate average sustainability scores by crop
    df = farm_data[farm_data['Crop_Type'].isin(selected_crops)].copy()
    sustainability = df.groupby('Crop_Type')['Sustainability_Score'].mean().reset_index()
    
    # Create the chart - use a radar chart to show multiple dimensions
    # For a demo, create distinct sub-scores for each crop
    result = []
    
    # Define unique modifiers for each crop to ensure variation
    crop_modifiers = {
        'Rice': {'water': 1.3, 'soil': 0.8, 'emissions': 1.1, 'biodiversity': 0.7},
        'Wheat': {'water': 0.9, 'soil': 1.2, 'emissions': 0.8, 'biodiversity': 1.1},
        'Maize': {'water': 1.1, 'soil': 0.9, 'emissions': 1.2, 'biodiversity': 0.8},
        'Cotton': {'water': 1.5, 'soil': 0.7, 'emissions': 0.7, 'biodiversity': 0.9},
        'Potato': {'water': 0.8, 'soil': 1.3, 'emissions': 0.9, 'biodiversity': 1.2},
        'Soybean': {'water': 0.7, 'soil': 1.1, 'emissions': 1.3, 'biodiversity': 1.0}
    }
    
    # Add default modifier for any crop not in our predefined list
    default_modifier = {'water': 1.0, 'soil': 1.0, 'emissions': 1.0, 'biodiversity': 1.0}
    
    for crop in sustainability['Crop_Type']:
        base_score = sustainability[sustainability['Crop_Type'] == crop]['Sustainability_Score'].iloc[0]
        
        # Get specific modifiers for this crop or use defaults
        modifier = crop_modifiers.get(crop, default_modifier)
        
        # Generate varied sub-scores based on the base score and crop-specific modifiers
        water_score = max(10, min(100, base_score * modifier['water']))
        soil_score = max(10, min(100, base_score * modifier['soil']))
        emission_score = max(10, min(100, base_score * modifier['emissions']))
        biodiversity_score = max(10, min(100, base_score * modifier['biodiversity']))
        
        result.append({
            'Crop_Type': crop,
            'Overall': base_score,
            'Water_Usage': water_score,
            'Soil_Health': soil_score,
            'Emissions': emission_score,
            'Biodiversity': biodiversity_score
        })
    
    sustainability_df = pd.DataFrame(result)
    
    # Create radar chart
    fig = go.Figure()
    
    for crop in sustainability_df['Crop_Type']:
        row = sustainability_df[sustainability_df['Crop_Type'] == crop].iloc[0]
        fig.add_trace(go.Scatterpolar(
            r=[row['Water_Usage'], row['Soil_Health'], row['Emissions'], row['Biodiversity'], row['Overall']],
            theta=['Water Usage', 'Soil Health', 'Emissions', 'Biodiversity', 'Overall'],
            fill='toself',
            name=crop
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Updated range to 0-100 for sustainability score
            )),
        showlegend=True,
        title='Sustainability Comparison'
    )
    
    # Convert to JSON for the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/weather')
def weather_page():
    """Display weather data and forecasts"""
    location = request.args.get('location', locations[0])
    
    # Get historical weather data
    historical = weather.get_historical_weather(location, months_back=6)
    
    # Get forecast data
    forecast = weather.get_weather_forecast(location, months_ahead=3)
    
    # Create temperature chart
    temp_fig = go.Figure()
    
    # Add historical data
    temp_fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['temperature_C'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue')
    ))
    
    # Add forecast data with confidence band
    temp_fig.add_trace(go.Scatter(
        x=forecast['date'],
        y=forecast['temperature_C'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', dash='dot')
    ))
    
    temp_fig.update_layout(
        title=f'Temperature for {location}',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified'
    )
    
    # Create rainfall chart
    rain_fig = go.Figure()
    
    # Add historical data
    rain_fig.add_trace(go.Bar(
        x=historical['date'],
        y=historical['rainfall_mm'],
        name='Historical',
        marker_color='blue'
    ))
    
    # Add forecast data
    rain_fig.add_trace(go.Bar(
        x=forecast['date'],
        y=forecast['rainfall_mm'],
        name='Forecast',
        marker_color='red'
    ))
    
    rain_fig.update_layout(
        title=f'Rainfall for {location}',
        xaxis_title='Date',
        yaxis_title='Rainfall (mm)',
        barmode='group',
        hovermode='x unified'
    )
    
    # Convert figures to JSON
    temp_chart = json.dumps(temp_fig, cls=plotly.utils.PlotlyJSONEncoder)
    rain_chart = json.dumps(rain_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template(
        'weather.html',
        location=location,
        locations=locations,
        temp_chart=temp_chart,
        rain_chart=rain_chart,
        forecast_data=forecast.to_dict('records')
    )

@app.route('/api/crop-rotation')
def api_crop_rotation():
    """API endpoint for crop rotation suggestions"""
    crop = request.args.get('crop', '')
    
    if not crop:
        return jsonify({"error": "No crop specified"})
    
    soil_health = {
        "N": int(request.args.get('nitrogen', 0)),
        "P": int(request.args.get('phosphorus', 0)),
        "K": int(request.args.get('potassium', 0))
    }
    
    rotation_plan = crop_rotation.suggest_rotation(crop, soil_health)
    formatted_plan = crop_rotation.format_rotation_plan(crop, rotation_plan)
    
    return jsonify({
        "crop": crop,
        "rotation_plan": formatted_plan,
        "soil_health": soil_health
    })

if __name__ == '__main__':
    app.run(debug=True) 