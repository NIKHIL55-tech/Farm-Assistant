import pandas as pd
from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher
from core.decision_engine import DecisionEngine

# Load the dataset
df = pd.read_csv("data/farmer_advisor_dataset.csv")

# Show available Farm_IDs
farm_ids = df["Farm_ID"].unique()
print(f"Available Farm_IDs: {farm_ids}\n")

# Ask user to input Farm_ID
selected_id = int(input("Enter a valid Farm_ID from the list above: "))

# Check if ID exists
if selected_id not in farm_ids:
    print("Invalid Farm_ID.")
    exit()

# Extract row for selected Farm_ID
farm_data = df[df["Farm_ID"] == selected_id].iloc[0]

# Get soil parameters
soil_ph = farm_data["Soil_pH"]
soil_moisture = farm_data["Soil_Moisture"]
temperature = farm_data["Temperature_C"]
rainfall = farm_data["Rainfall_mm"]

# Formulate query for decision engine
query = {
    "query": f"Recommend crops for pH {soil_ph}, moisture {soil_moisture}, temperature {temperature}, rainfall {rainfall}"
}

# Initialize agents and decision engine
agents = [FarmerAdvisor(name="FarmerAdvisor"), MarketResearcher(name="MarketResearcher")]
engine = DecisionEngine(agents)

# Get the result
result = engine.run(query)

# Display result
if "recommendation" in result:
    print("\n=== Final Recommendation ===")
    print(result["recommendation"])
else:
    print("No valid response.")
