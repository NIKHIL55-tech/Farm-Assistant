# 🌾 Multi-Agentic AI for Sustainable Agriculture

A hackathon project aiming to improve farming efficiency and reduce environmental impact using a SQLite-backed multi-agent AI system.

## ✅ Completed Phases

### Phase 1: Core Infrastructure ✓
- SQLite database created and loaded with real datasets
- Agent framework for communication
- Logging setup for traceability

### Phase 2: MVP Agents ✓
- Implemented FarmerAdvisor with farm data analysis and recommendation capabilities
- Built MarketResearcher with price trend analysis and profitability calculations
- Connected agents to database for information retrieval
- Created basic inter-agent communication workflow

### Phase 3: Agent Coordination & Decision Engine ✓
- Implemented Coordinator module with weighted recommendation system
- Created algorithm to balance economic and environmental factors
- Built Decision Engine with sustainability scoring
- Developed recommendation aggregation functionality

### Phase 4: Enhanced Features & UI ✓
- Added crop rotation suggestions with multi-year planning
- Implemented weather data integration with forecasting
- Created yield prediction models using machine learning
- Built web interface with interactive dashboards and data visualizations
- Added environmental impact analysis and sustainability metrics (scale 0-100)
- Integrated Plotly for interactive data visualizations

## 🚀 Agents

- **FarmerAdvisor**: Analyzes farm data and provides crop recommendations based on soil conditions
- **MarketResearcher**: Examines market trends, calculates crop profitability, and forecasts prices

## 📊 Advanced Features

- **Crop Rotation Planner**: Suggests optimal crop rotation sequences based on soil health and crop compatibility
- **Weather Integration**: Provides historical weather data and forecasts with increasing uncertainty over time
- **Yield Prediction**: Machine learning models for predicting crop yields based on farm conditions
- **Sustainability Metrics**: Visual dashboards showing environmental impact of different crop choices (0-100 scale)
- **Data Visualization**: Interactive charts using Plotly for price trends, sustainability comparisons, and weather data

## 📂 Usage

```bash
# Setup
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python database/init_db.py

# Run the web application
python run_app.py

# Run the phase 2 demo
python test_phase2.py

# Run the decision engine test
python run_decision_test.py
```

## Dependencies

This project requires the following main dependencies:
- Flask: Web framework
- Pandas: Data manipulation
- Scikit-learn: Machine learning models
- Plotly: Interactive data visualization
- SQLite: Database storage

Install all dependencies using the requirements.txt file.

## 🌐 Web Interface

The web interface is available at http://localhost:5000 and includes:

1. **Dashboard**: Overview of farm statistics, crop performance, and market prices
2. **Farm Input Form**: Enter farm details to get personalized recommendations
3. **Recommendation Page**: Detailed crop recommendations with sustainability metrics
4. **Weather Analysis**: Historical and forecasted weather data with agricultural impact analysis
5. **Crop Rotation Planner**: Interactive tool for planning sustainable crop rotations

## Next Steps

The project is now ready for Phase 5: Polish & Presentation. Key activities include:
- Comprehensive testing with various farm conditions
- Fixing minor UI issues
- Optimizing performance
- Preparing demonstration data
- Creating presentation materials

# Agricultural Intelligence Network (AIN): Phased Development Plan

Given your 2-day hackathon timeframe, here's a pragmatic phased development approach that ensures you have a working deliverable at each milestone:

## Phase 1: Core Infrastructure (4 hours)
**Goal:** Create the foundation that everything else will build upon

1. **Set up SQLite Database**
   - Create basic tables for farms, markets, crops
   - Import your existing datasets
   - Establish simple relationships

2. **Agent Framework Skeleton**
   - Define base agent class with communication methods
   - Create simple message passing between agents
   - Set up logging for debugging

**Deliverable:** Working database with imported data and basic agent framework that can pass messages

## Phase 2: MVP Agents (6 hours)
**Goal:** Implement the two required agents with basic functionality

1. **Farmer Advisor Agent**
   - Implement basic farm data analysis
   - Create simple recommendation logic based on farm characteristics
   - Connect to database for farm information

2. **Market Researcher Agent**
   - Build price trend analysis from your market dataset
   - Implement basic profitability calculations
   - Connect to database for market information

**Deliverable:** Two functioning agents that can provide basic independent recommendations

## Phase 3: Agent Coordination & Decision Engine (6 hours)
**Goal:** Enable agents to work together with basic consensus mechanism

1. **Coordinator Module**
   - Implement weighted recommendation system
   - Create simple algorithm to balance economic and environmental factors
   - Build basic conflict resolution logic

2. **Decision Engine**
   - Develop recommendation aggregation
   - Create simple scoring for sustainability metrics
   - Implement basic visualization of recommendations

**Deliverable:** End-to-end system that provides unified recommendations based on multiple agent inputs

## Phase 4: Enhanced Features & UI (8 hours)
**Goal:** Add differentiating features and user interface

1. **Enhanced Functionality**
   - Implement crop rotation suggestions
   - Add weather data integration (even simulated)
   - Build simple prediction models for yields

2. **Simple Web Interface**
   - Create basic input forms for farm data
   - Build recommendation display dashboards
   - Add simple visualization of environmental impacts

**Deliverable:** User-facing application with advanced recommendations and basic UI

## Phase 5: Polish & Presentation (remainder of time)
**Goal:** Prepare for demo and final submission

1. **Testing & Bug Fixes**
   - Create test cases with sample farms
   - Fix critical bugs
   - Optimize performance bottlenecks

2. **Demo Preparation**
   - Prepare compelling example cases
   - Create brief presentation slides
   - Practice demonstration flow

**Deliverable:** Polished application ready for demonstration

## Phase 6: Future Enhancements (Post-Hackathon)
**Goal:** Address remaining challenges from the problem statement and expand system capabilities

1. **Additional Stakeholder Agents**
   - Implement Agricultural Expert agent for specialized knowledge
   - Add Government Policy agent to incorporate regulations and subsidies
   - Create Consumer Trend agent to track changing market preferences

2. **Advanced Environmental Impact Analysis**
   - Develop carbon footprint calculation for farming practices
   - Implement water consumption optimization models
   - Create soil erosion prevention strategies with actionable recommendations

3. **Community and Knowledge Sharing Platform**
   - Build collaborative features between farmers
   - Implement success story sharing mechanism
   - Create regional best practices repository

4. **Real-time Data Integration**
   - Connect to real-time weather APIs for live forecasts
   - Implement IoT sensor integration for live farm monitoring
   - Add satellite imagery analysis for crop health monitoring

5. **Climate Change Adaptation Strategies**
   - Develop long-term climate projections for farming regions
   - Create adaptive farming strategy recommendations
   - Build resilience scoring for different crop combinations

**Deliverable:** Comprehensive agricultural intelligence platform addressing environmental, economic, and social aspects of sustainable farming

## Contingency Features
If you find yourself ahead of schedule, consider adding these features in order of priority:

1. Simple machine learning for crop yield prediction
2. Interactive scenario comparison tool
3. Visualization of environmental impact metrics
4. Historical recommendation tracking

This phased approach ensures you'll have something functional to present even if you run into unexpected challenges along the way. Each phase builds upon the previous one while delivering a working system.


##update setuptools
#> python -m pip install --upgrade setuptools