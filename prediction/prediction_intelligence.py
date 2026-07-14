"""
prediction_intelligence.py

Convert raw VOLTERA model predictions into
validated battery prediction intelligence.
"""


def validate_prediction(
    current_battery,
    predicted_battery,
    is_charging=False
):
    """
    Validate and constrain a battery prediction
    to physically meaningful values.
    """

    # Battery percentage must stay between 0 and 100
    predicted_battery = max(
        0,
        min(100, predicted_battery)
    )

    # During discharge, future battery should not
    # exceed the current battery percentage
    if not is_charging:
        predicted_battery = min(
            current_battery,
            predicted_battery
        )

    return predicted_battery

def generate_prediction_intelligence(
    current_battery,
    predicted_battery,
    prediction_horizon_minutes,
    is_charging=False
):
    """
    Convert a raw battery prediction into
    useful VOLTERA prediction intelligence.
    """

    validated_prediction = validate_prediction(
        current_battery,
        predicted_battery,
        is_charging
    )

    expected_change = (
        validated_prediction - current_battery
    )

    if is_charging:
        status = "Charging"
    elif expected_change < 0:
        status = "Battery Draining"
    else:
        status = "Battery Stable"

    return {
        "current_battery": current_battery,
        "predicted_battery": validated_prediction,
        "prediction_horizon_minutes": prediction_horizon_minutes,
        "expected_change": expected_change,
        "status": status
    }