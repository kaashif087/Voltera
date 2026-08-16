"""
VOLTERA - Recommendation Notification Adapter

Converts Recommendation Engine outputs into the
recommendation names understood by Notification Engine.
"""


RECOMMENDATION_TO_NOTIFICATION = {

    "CRITICAL_BATTERY":
        "Critical Battery Level",

    "LOW_BATTERY":
        "Low Battery Level",

    "RAPID_DRAIN":
        "Rapid Battery Drain",

    "HIGH_SYSTEM_LOAD":
        "High System Load",

    "HIGH_BATTERY_CHARGING":
        "High Battery While Charging",

    "NORMAL_CHARGING":
        "Charging Normally",

    "BATTERY_STABLE":
        "Battery Stable",

    "PREDICTED_CRITICAL_BATTERY":
        "Predicted Critical Battery",

    "PREDICTED_LOW_BATTERY":
        "Predicted Low Battery",

    "SIGNIFICANT_FUTURE_DRAIN":
        "Rapid Battery Drain",

    "BATTERY_FORECAST_STABLE":
        "Battery Stable",
}


def adapt_recommendation(recommendation):
    """
    Convert a Recommendation Engine result into the
    recommendation name expected by Notification Engine.

    Args:
        recommendation:
            Recommendation Engine result dictionary.

    Returns:
        str | None
    """

    if recommendation is None:
        return None

    if not isinstance(recommendation, dict):
        raise TypeError(
            "recommendation must be a dictionary"
        )

    situation = recommendation.get("situation")

    if situation is None:
        raise ValueError(
            "recommendation is missing 'situation'"
        )

    return RECOMMENDATION_TO_NOTIFICATION.get(
        situation
    )