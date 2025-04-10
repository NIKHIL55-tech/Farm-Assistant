# run_decision_test.py

import pandas as pd
from agents.farmer_advisor import FarmerAdvisor

# Load dataset
df = pd.read_csv("data/farmer_advisor_dataset.csv")
print("Available Farm_IDs:", df["Farm_ID"].unique())

# Choose a valid Farm_ID to test
farm_id = df["Farm_ID"].iloc[0]  # or manually set, e.g., farm_id = "F001"

# Create a message dictionary including farm_id
message = {
    "query": f"Recommend crops for Farm_ID {farm_id}",
    "farm_id": farm_id
}

# Run FarmerAdvisor agent
advisor = FarmerAdvisor("FarmerAdvisor")
response = advisor.run(message)

# Output the result
print("\n=== Farmer Advisor Recommendation ===")
print(response["response"])
print("Top Crops:", response["recommended_crops"])
if "detailed" in response:
    for crop in response["detailed"]:
        print(f"- {crop['Crop_Type']} (Avg Yield: {crop['Avg_Yield']:.2f} tons, Samples: {crop['Sample_Count']})")
