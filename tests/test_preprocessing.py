from prediction.predictor import run_prediction_pipeline


results = run_prediction_pipeline(
    "data/battery_log.csv"
)

print("VOLTERA Prediction Pipeline")
print("===========================")

print("Actual values:")
print(results["actual_values"])

print("\nPredicted values:")
print(results["predictions"])

print("\nMAE:", round(results["mae"], 2))
print("RMSE:", round(results["rmse"], 2))
