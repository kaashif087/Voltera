"""
VOLTERA Input Validator

This module validates battery context before it enters
the Recommendation Engine.

Design Goals:
- Validate required fields
- Validate data types
- Validate value ranges
- Raise clear exceptions
"""


REQUIRED_FIELDS = [
    "battery_percentage",
    "charging",
    "cpu_usage",
    "ram_usage",
    "predicted_battery",
    "prediction_horizon_minutes",
    "expected_change"
]


def validate_battery_context(battery_context):
    """
    Validate the battery context dictionary.

    Args:
        battery_context (dict):
            Battery information supplied to the
            recommendation engine.

    Raises:
        KeyError:
            If a required field is missing.

        TypeError:
            If a field has an invalid type.

        ValueError:
            If a numeric value is outside
            the valid range.
    """

    # -----------------------------
    # Required fields
    # -----------------------------
    for field in REQUIRED_FIELDS:
        if field not in battery_context:
            raise KeyError(
                f"Missing required field: '{field}'"
            )

    # -----------------------------
    # Battery Percentage
    # -----------------------------
    battery = battery_context["battery_percentage"]

    if not isinstance(battery, (int, float)):
        raise TypeError(
            "battery_percentage must be numeric."
        )

    if not 0 <= battery <= 100:
        raise ValueError(
            "battery_percentage must be between 0 and 100."
        )

    # -----------------------------
    # Charging
    # -----------------------------
    charging = battery_context["charging"]

    if not isinstance(charging, bool):
        raise TypeError(
            "charging must be True or False."
        )

    # -----------------------------
    # CPU Usage
    # -----------------------------
    cpu = battery_context["cpu_usage"]

    if not isinstance(cpu, (int, float)):
        raise TypeError(
            "cpu_usage must be numeric."
        )

    if not 0 <= cpu <= 100:
        raise ValueError(
            "cpu_usage must be between 0 and 100."
        )

    # -----------------------------
    # RAM Usage
    # -----------------------------
    ram = battery_context["ram_usage"]

    if not isinstance(ram, (int, float)):
        raise TypeError(
            "ram_usage must be numeric."
        )

    if not 0 <= ram <= 100:
        raise ValueError(
            "ram_usage must be between 0 and 100."
        )

    # -----------------------------
    # Predicted Battery
    # -----------------------------
    predicted = battery_context["predicted_battery"]

    if not isinstance(predicted, (int, float)):
        raise TypeError(
            "predicted_battery must be numeric."
        )

    if not 0 <= predicted <= 100:
        raise ValueError(
            "predicted_battery must be between 0 and 100."
        )

    # -----------------------------
    # Prediction Horizon
    # -----------------------------
    horizon = battery_context[
        "prediction_horizon_minutes"
    ]

    if not isinstance(horizon, (int, float)):
        raise TypeError(
            "prediction_horizon_minutes must be numeric."
        )

    if horizon < 0:
        raise ValueError(
            "prediction_horizon_minutes cannot be negative."
        )

    # -----------------------------
    # Expected Change
    # -----------------------------
    expected_change = battery_context["expected_change"]

    if not isinstance(expected_change, (int, float)):
        raise TypeError(
            "expected_change must be numeric."
        )