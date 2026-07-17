import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from recommendation.recommendation_engine import (
    generate_recommendation
)


def run_test(name, context):

    print("\n" + "=" * 60)
    print(f"Test : {name}")
    print("=" * 60)

    try:

        result = generate_recommendation(context)

        print("PASS")
        print(result)

    except Exception as error:

        print("Handled Exception")
        print(type(error).__name__)
        print(error)


test_cases = [

    (
        "Empty Context",
        {}
    ),

    (
        "Missing Predicted Battery",
        {
            "battery_percentage": 50,
            "charging": False,
            "cpu_usage": 40,
            "ram_usage": 35,
            "expected_change": -5
        }
    ),

    (
        "Missing CPU",
        {
            "battery_percentage": 50,
            "charging": False,
            "ram_usage": 40,
            "predicted_battery": 45,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Missing RAM",
        {
            "battery_percentage": 50,
            "charging": False,
            "cpu_usage": 30,
            "predicted_battery": 45,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Negative Battery",
        {
            "battery_percentage": -5,
            "charging": False,
            "cpu_usage": 30,
            "ram_usage": 30,
            "predicted_battery": -10,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Battery Above 100",
        {
            "battery_percentage": 150,
            "charging": False,
            "cpu_usage": 20,
            "ram_usage": 20,
            "predicted_battery": 145,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Invalid Battery Type",
        {
            "battery_percentage": "Fifty",
            "charging": False,
            "cpu_usage": 20,
            "ram_usage": 20,
            "predicted_battery": 45,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Battery None",
        {
            "battery_percentage": None,
            "charging": False,
            "cpu_usage": 20,
            "ram_usage": 20,
            "predicted_battery": 40,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    ),

    (
        "Multiple Serious Problems",
        {
            "battery_percentage": 5,
            "charging": False,
            "cpu_usage": 95,
            "ram_usage": 95,
            "predicted_battery": 2,
            "prediction_horizon_minutes": 30,
            "expected_change": -25
        }
    )

]

print("\n==============================================")
print("Recommendation Edge Case Test Suite")
print("==============================================")

for name, context in test_cases:
    run_test(name, context)

print("\n==============================================")
print("Edge Case Tests Completed")
print("==============================================")