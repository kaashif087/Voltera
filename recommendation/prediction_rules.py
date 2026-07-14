"""
VOLTERA Prediction Recommendation Rules

This module creates recommendations based on
future battery predictions.

Input:
    Prediction intelligence data:

    {
        "current_battery": float,
        "predicted_battery": float,
        "prediction_horizon_minutes": int,
        "expected_change": float
    }

Output:
    Prediction-aware recommendation details.

Design Goals:
    - Time-aware decisions
    - Explainable predictions
    - Integration with recommendation engine
    - Future JARVIS compatibility
"""
PREDICTION_THRESHOLDS = {
    "PREDICTED_CRITICAL_BATTERY": 4,
    "SIGNIFICANT_FUTURE_DRAIN": 3,
    "PREDICTED_LOW_BATTERY": 2,
    "BATTERY_FORECAST_STABLE": 1
}

def assess_prediction_state(
    current_battery,
    predicted_battery,
    expected_change
):
    """
    Assess future battery behavior.

    Args:
        current_battery (float):
            Current battery percentage.

        predicted_battery (float):
            Predicted future battery percentage.

        expected_change (float):
            Expected battery percentage change.

    Returns:
        str:
            Prediction situation.
        None:
            If no prediction concern exists.
    """

    if predicted_battery <= 10 and current_battery > 10:
        return "PREDICTED_CRITICAL_BATTERY"

    if predicted_battery <= 20 and current_battery > 20:
        return "PREDICTED_LOW_BATTERY"

    if expected_change <= -15:
        return "SIGNIFICANT_FUTURE_DRAIN"

    if expected_change > -5:
        return "BATTERY_FORECAST_STABLE"

    return None


def get_prediction_recommendation(state):
    """Return a recommendation detail for a given prediction state."""
    return PREDICTION_RECOMMENDATIONS.get(state)

PREDICTION_RECOMMENDATIONS = {

    "PREDICTED_CRITICAL_BATTERY": {
        "priority": "CRITICAL",
        "title": "Critical Battery Expected Soon",
        "recommendation": (
            "Your battery is expected to reach a critical "
            "level soon. Consider charging now."
        ),
        "reason": (
            "Prediction shows the battery may fall below "
            "10% within the prediction period."
        )
    },

    "PREDICTED_LOW_BATTERY": {
        "priority": "HIGH",
        "title": "Low Battery Expected Soon",
        "recommendation": (
            "Your battery is expected to become low soon. "
            "Plan charging before important tasks."
        ),
        "reason": (
            "Prediction shows the battery may fall below "
            "20%."
        )
    },

    "SIGNIFICANT_FUTURE_DRAIN": {
        "priority": "HIGH",
        "title": "Future Battery Drain Detected",
        "recommendation": (
            "A significant battery drop is expected. "
            "Avoid heavy tasks if possible."
        ),
        "reason": (
            "Prediction detected a large battery decrease "
            "in the upcoming period."
        )
    },

    "BATTERY_FORECAST_STABLE": {
        "priority": "LOW",
        "title": "Battery Forecast Stable",
        "recommendation": (
            "Your battery is expected to remain stable."
        ),
        "reason": (
            "No significant future battery concern detected."
        )
    }

}


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
