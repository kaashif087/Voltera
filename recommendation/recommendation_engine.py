import recommendation
from recommendation.prediction_rules import (
    assess_prediction_state,
    get_prediction_recommendation
)

from recommendation.recommendation_rules import (
    get_recommendation_rule
)

from recommendation.priority_manager import (
    get_highest_priority_recommendation
)

from recommendation.situation_assessor import (
    assess_battery_level,
    assess_charging_status,
    assess_prediction,
    assess_system_load
)

"""
VOLTERA Recommendation Engine

This module acts as the main coordinator for the battery recommendation system.

Input Contract:
    The recommendation engine receives a battery_context dictionary containing:

    {
        "battery_percentage": float,
        "charging": bool,
        "cpu_usage": float,
        "ram_usage": float,
        "predicted_battery": float,
        "prediction_horizon_minutes": int,
        "expected_change": float,
        "prediction_status": str
    }

Output Contract:
    The recommendation engine returns a structured recommendation dictionary:

    {
        "situation": str,
        "priority": str,
        "recommendation": str,
        "reason": str
    }

The engine will coordinate:
    1. Battery situation assessment
    2. Recommendation rule evaluation
    3. Recommendation priority selection
    4. Final user-friendly recommendation generation

Design Goals:
    - Modular
    - Scalable
    - Explainable
    - Reusable
    - Easy to integrate with future VOLTERA modules and JARVIS

    Prediction Awareness:

The engine can use prediction intelligence to improve
recommendations by considering:

    - Current battery level
    - Predicted battery level
    - Prediction time horizon
    - Expected battery change

Prediction data helps VOLTERA provide
time-aware battery decisions.

"""

def generate_recommendation(battery_context):
    """
    Generate the final VOLTERA recommendation.

    Args:
        battery_context (dict):
            Current battery and prediction information.

    Returns:
        dict:
            Final recommendation output.
        None:
            If no recommendation exists.
    """

    situations = []

    battery_situation = assess_battery_level(
        battery_context["battery_percentage"],
        battery_context["charging"]
    )
    if battery_situation:
        situations.append(battery_situation)

    charging_situation = assess_charging_status(
        battery_context["battery_percentage"],
        battery_context["charging"]
    )
    if charging_situation:
        situations.append(charging_situation)

    system_situation = assess_system_load(
        battery_context["cpu_usage"],
        battery_context["ram_usage"]
    )
    if system_situation:
        situations.append(system_situation)

    prediction_situation = assess_prediction_state(
        battery_context["battery_percentage"],
        battery_context["predicted_battery"],
        battery_context["expected_change"]
    )
    if prediction_situation:
        situations.append(prediction_situation)

    if not situations:
        return None

    selected_situation = get_highest_priority_recommendation(situations)
    if selected_situation.startswith("PREDICTED") or selected_situation in [
    "SIGNIFICANT_FUTURE_DRAIN",
    "BATTERY_FORECAST_STABLE"
]:
        recommendation = get_prediction_recommendation(
            selected_situation
        )
    else:
        recommendation = get_recommendation_rule(
            selected_situation
        )

    print("All Detected Situations:", situations)
    print("Selected Situation:", selected_situation)
    print("Recommendation:", recommendation)

    return recommendation

