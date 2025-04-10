def calculate_sustainability_score(row):
    score = 0
    score += (1 - abs(row["Soil_pH"] - 6.5) / 6.5) * 25
    score += (1 - abs(row["Soil_Moisture"] - 25) / 25) * 25
    score += (1 - abs(row["Temperature_C"] - 30) / 30) * 25
    score += (1 - abs(row["Rainfall_mm"] - 100) / 100) * 25
    return max(0, min(score, 100))
