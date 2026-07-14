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

