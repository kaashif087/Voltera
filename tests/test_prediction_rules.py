import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from recommendation.prediction_rules import (
    assess_prediction_state,
    get_prediction_recommendation
)


def print_result(test_name, expected, result):
    status = "PASS" if expected == result else "FAIL"

    print(test_name)
    print("Expected :", expected)
    print("Got      :", result)
    print("Result   :", status)
    print("-" * 50)


print("\n===================================")
print("Prediction Rules Test Suite")
print("===================================\n")


# ----------------------------------------
# Prediction State Tests
# ----------------------------------------

prediction_tests = [

    (25, 8, -17, "PREDICTED_CRITICAL_BATTERY"),

    (45, 18, -12, "PREDICTED_LOW_BATTERY"),

    (70, 55, -18, "SIGNIFICANT_FUTURE_DRAIN"),

    (65, 63, -2, "BATTERY_FORECAST_STABLE"),

    (15, 12, -8, None),
]

print("Prediction State Tests\n")

for current, predicted, change, expected in prediction_tests:

    result = assess_prediction_state(
        current,
        predicted,
        change
    )

    print_result(
        f"Current={current}% Predicted={predicted}% Change={change}",
        expected,
        result
    )


# ----------------------------------------
# Recommendation Lookup Tests
# ----------------------------------------

print("\nRecommendation Lookup Tests\n")

states = [

    "PREDICTED_CRITICAL_BATTERY",

    "PREDICTED_LOW_BATTERY",

    "SIGNIFICANT_FUTURE_DRAIN",

    "BATTERY_FORECAST_STABLE",

    "UNKNOWN"
]

for state in states:

    recommendation = get_prediction_recommendation(state)

    status = "PASS"

    if state == "UNKNOWN":
        expected = None
    else:
        expected = "Dictionary"

        if recommendation is None:
            status = "FAIL"

    print(f"State    : {state}")
    print(f"Returned : {recommendation}")
    print(f"Result   : {status}")
    print("-" * 50)


print("\n===================================")
print("Prediction Rules Tests Completed")
print("===================================")