"""
VOLTERA Recommendation Rules

This module maps detected battery situations into
user-friendly recommendations.

Input:
    Detected battery situations from situation_assessor.py

Output:
    Structured recommendation information containing:

    {
        "situation": str,
        "priority": str,
        "title": str,
        "recommendation": str,
        "reason": str
    }

Design Goals:
    - Explainable recommendations
    - Easy rule expansion
    - Reusable for mobile notifications
    - Future integration with JARVIS
"""

RECOMMENDATION_RULES = {

    "CRITICAL_BATTERY": {
        "priority": "CRITICAL",
        "title": "Critical Battery Level",
        "recommendation": (
            "Connect your charger immediately to avoid "
            "battery shutdown."
        ),
        "reason": (
            "Battery level is critically low and the device "
            "needs power."
        )
    },

    "LOW_BATTERY": {
        "priority": "HIGH",
        "title": "Low Battery Level",
        "recommendation": (
            "Consider charging your device before starting "
            "power-intensive tasks."
        ),
        "reason": (
            "Battery level is low and may not support "
            "extended usage."
        )
    },

    "RAPID_DRAIN": {
        "priority": "HIGH",
        "title": "Rapid Battery Drain Detected",
        "recommendation": (
            "Your battery is draining quickly. "
            "Consider reducing heavy tasks or connecting the charger."
        ),
        "reason": (
            "Prediction intelligence detected a significant "
            "battery drop in a short time."
        )
    },

    "HIGH_BATTERY_CHARGING": {
        "priority": "MEDIUM",
        "title": "Battery Above 80% While Charging",
        "recommendation": (
            "You may disconnect the charger to reduce "
            "unnecessary prolonged charging."
        ),
        "reason": (
            "Battery level is already high while the device "
            "continues charging."
        )
    },

    "NORMAL_CHARGING": {
        "priority": "LOW",
        "title": "Charging Normally",
        "recommendation": (
            "Your device is charging normally."
        ),
        "reason": (
            "Battery is charging within a normal range."
        )
    },

    "HIGH_SYSTEM_LOAD": {
        "priority": "MEDIUM",
        "title": "High System Load Detected",
        "recommendation": (
            "Consider closing unnecessary applications "
            "to improve battery efficiency."
        ),
        "reason": (
            "High CPU or RAM usage may increase battery drain."
        )
    },

    "BATTERY_STABLE": {
        "priority": "LOW",
        "title": "Battery Stable",
        "recommendation": (
            "Your battery usage looks normal."
        ),
        "reason": (
            "No significant battery issue was detected."
        )
    }

}

def get_recommendation_rule(situation):
    """
    Retrieve recommendation details for a given situation.

    Args:
        situation (str):
            Detected battery situation.

    Returns:
        dict:
            Recommendation details if rule exists.
        None:
            If no rule is available.
    """

    return RECOMMENDATION_RULES.get(situation)