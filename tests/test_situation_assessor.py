import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from recommendation.situation_assessor import (
    assess_battery_level,
    assess_charging_status,
    assess_prediction,
    assess_system_load
)


def print_result(test_name, expected, result):
    status = "PASS" if expected == result else "FAIL"

    print(f"{test_name}")
    print(f"Expected : {expected}")
    print(f"Got      : {result}")
    print(f"Result   : {status}")
    print("-" * 50)


print("\n==============================")
print("Situation Assessor Test Suite")
print("==============================\n")


# ==========================================================
# Battery Level Tests
# ==========================================================

print("Battery Level Tests\n")

battery_tests = [
    (5, False, "CRITICAL_BATTERY"),
    (10, False, "CRITICAL_BATTERY"),
    (15, False, "LOW_BATTERY"),
    (20, False, "LOW_BATTERY"),
    (25, False, None),
    (5, True, None),
]

for battery, charging, expected in battery_tests:
    result = assess_battery_level(
        battery,
        charging
    )

    print_result(
        f"Battery={battery}% Charging={charging}",
        expected,
        result
    )


# ==========================================================
# Charging Status Tests
# ==========================================================

print("\nCharging Status Tests\n")

charging_tests = [
    (90, True, "HIGH_BATTERY_CHARGING"),
    (80, True, "HIGH_BATTERY_CHARGING"),
    (79, True, "NORMAL_CHARGING"),
    (45, True, "NORMAL_CHARGING"),
    (90, False, None),
]

for battery, charging, expected in charging_tests:

    result = assess_charging_status(
        battery,
        charging
    )

    print_result(
        f"Battery={battery}% Charging={charging}",
        expected,
        result
    )


# ==========================================================
# Prediction Tests
# ==========================================================

print("\nPrediction Tests\n")

prediction_tests = [
    (-15, "RAPID_DRAIN"),
    (-10, "RAPID_DRAIN"),
    (-9, None),
    (0, None),
    (5, None),
]

for predicted_change, expected in prediction_tests:

    result = assess_prediction(
        predicted_change
    )

    print_result(
        f"Predicted Change={predicted_change}",
        expected,
        result
    )


# ==========================================================
# System Load Tests
# ==========================================================

print("\nSystem Load Tests\n")

system_load_tests = [
    (90, 50, "HIGH_SYSTEM_LOAD"),
    (50, 90, "HIGH_SYSTEM_LOAD"),
    (80, 40, "HIGH_SYSTEM_LOAD"),
    (40, 85, "HIGH_SYSTEM_LOAD"),
    (79, 84, None),
    (70, 70, None),
]

for cpu, ram, expected in system_load_tests:

    result = assess_system_load(
        cpu,
        ram
    )

    print_result(
        f"CPU={cpu}% RAM={ram}%",
        expected,
        result
    )


print("\n=========================================")
print("Situation Assessor Tests Completed")
print("=========================================")