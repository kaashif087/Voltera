from prediction.predictor import predict_battery

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

prediction = predict_battery(sample)

print("=" * 40)
print("VOLTERA Predictor Test")
print("=" * 40)
print(f"Predicted Battery Percentage: {prediction:.2f}%")