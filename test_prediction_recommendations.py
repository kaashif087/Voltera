from recommendation.prediction_rules import (
    get_prediction_recommendation
)


test_states = [
    "PREDICTED_CRITICAL_BATTERY",
    "PREDICTED_LOW_BATTERY",
    "SIGNIFICANT_FUTURE_DRAIN",
    "BATTERY_FORECAST_STABLE",
    "UNKNOWN"
]


for state in test_states:

    result = get_prediction_recommendation(state)

    print("\nState:", state)
    print("Result:", result)