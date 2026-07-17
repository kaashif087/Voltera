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


def print_result(test_name, expected, result):
    status = "PASS" if expected == result else "FAIL"

    print(f"\n{test_name}")
    print(f"Expected : {expected}")
    print(f"Got      : {result}")
    print(f"Result   : {status}")
    print("-" * 50)


print("\n======================================")
print("Recommendation Engine Test Suite")
print("======================================")

test_cases = [

    {
        "name": "Critical Battery",
        "context": {
            "battery_percentage": 5,
            "charging": False,
            "cpu_usage": 30,
            "ram_usage": 40,
            "predicted_battery": 5,
            "prediction_horizon_minutes": 30,
            "expected_change": -2
        },
        "expected": "Critical Battery Level"
    },

    {
        "name": "Low Battery",
        "context": {
            "battery_percentage": 18,
            "charging": False,
            "cpu_usage": 30,
            "ram_usage": 40,
            "predicted_battery": 17,
            "prediction_horizon_minutes": 30,
            "expected_change": -2
        },
        "expected": "Low Battery Level"
    },

    {
        "name": "Predicted Critical Battery",
        "context": {
            "battery_percentage": 25,
            "charging": False,
            "cpu_usage": 40,
            "ram_usage": 40,
            "predicted_battery": 8,
            "prediction_horizon_minutes": 30,
            "expected_change": -17
        },
        "expected": "Critical Battery Expected Soon"
    },

    {
        "name": "High System Load",
        "context": {
            "battery_percentage": 60,
            "charging": False,
            "cpu_usage": 95,
            "ram_usage": 40,
            "predicted_battery": 58,
            "prediction_horizon_minutes": 30,
            "expected_change": -2
        },
        "expected": "High System Load Detected"
    }

]

for test in test_cases:

    recommendation = generate_recommendation(
        test["context"]
    )

    title = None

    if recommendation:
        title = recommendation["title"]

    print_result(
        test["name"],
        test["expected"],
        title
    )

print("\n======================================")
print("Recommendation Engine Tests Completed")
print("======================================")