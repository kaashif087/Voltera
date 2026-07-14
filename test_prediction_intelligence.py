from prediction.predictor import get_prediction_intelligence


sample = {
    "Battery_Percentage": 60,
    "CPU_Usage": 10,
    "RAM_Usage": 70,
    "Hour": 15,
    "Day_Of_Week": 6,
    "Battery_Drain_Rate": 0.15,
    "Rolling_CPU_Average": 12,
    "Rolling_RAM_Average": 68,
    "Prediction_Horizon_Minutes": 10
}

result = get_prediction_intelligence(
    sample,
    is_charging=False
)

print("=" * 45)
print("VOLTERA PREDICTION INTELLIGENCE TEST")
print("=" * 45)

print(f"Current Battery    : {result['current_battery']:.2f}%")
print(f"Predicted Battery  : {result['predicted_battery']:.2f}%")
print(
    f"Prediction Horizon : "
    f"{result['prediction_horizon_minutes']:.0f} minutes"
)
print(f"Expected Change    : {result['expected_change']:.2f}%")
print(f"Status             : {result['status']}")
