def predict_congestion(vehicle_count, heavy_count):
    # Calculate a simple traffic score
    traffic_score = vehicle_count + (heavy_count * 2)

    if traffic_score <= 4:
        congestion = "Low"
    elif traffic_score <= 8:
        congestion = "Medium"
    else:
        congestion = "High"

    return congestion, traffic_score


# Test with current detection
vehicle_count = 4
heavy_count = 1

congestion, score = predict_congestion(vehicle_count, heavy_count)

print("\n===== UrbanTwin AI Congestion Prediction =====")
print("Total Vehicles:", vehicle_count)
print("Heavy Vehicles:", heavy_count)
print("Traffic Score:", score)
print("Congestion Level:", congestion)
print("==============================================")