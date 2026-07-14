from recommendation.recommendation_engine import (
    generate_recommendation
)


battery_context = {
    "battery_percentage": 25,
    "charging": False,
    "cpu_usage": 40,
    "ram_usage": 40,
    "predicted_battery": 8,
    "prediction_horizon_minutes": 30,
    "expected_change": -17
}

result = generate_recommendation(
    battery_context
)


print("Detected Situations:")
print(result)