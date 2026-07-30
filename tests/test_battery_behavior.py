from learning.learning_manager import LearningManager
from learning.battery_behavior import BatteryBehavior


print("\n======================================")
print("Battery Behavior Test Suite")
print("======================================\n")


manager = LearningManager("tests/test_learning_data.json")

manager.reset_learning_data()

behavior = BatteryBehavior(manager)


def run_test(test_name, expected, actual):
    print(test_name)
    print(f"Expected : {expected}")
    print(f"Got      : {actual}")

    if expected == actual:
        print("Result   : PASS")
    else:
        print("Result   : FAIL")

    print("-" * 50)


run_test(
    "BatteryBehavior Object Creation",
    True,
    isinstance(behavior, BatteryBehavior)
)

import pandas as pd

sample_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 09:00:00",
            "2026-07-28 10:00:00",
            "2026-07-28 11:00:00",
            "2026-07-28 12:00:00",
        ],

        "Battery_Percentage": [
            100,
            90,
            80,
            70
        ],

        "Charging_Status": [
            False,
            False,
            False,
            False
        ]
    }
)

average_drain = behavior.learn_average_drain_rate(
    sample_data
)

run_test(
    "Learn Average Drain Rate",
    10.0,
    average_drain
)

charging_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 20:00:00",
            "2026-07-28 21:00:00",
            "2026-07-28 22:00:00",
        ],

        "Battery_Percentage": [
            40,
            60,
            80
        ],

        "Charging_Status": [
            True,
            True,
            True
        ]
    }
)

average_speed = behavior.learn_average_charging_speed(
    charging_data
)

run_test(
    "Learn Average Charging Speed",
    20.0,
    average_speed
)

heavy_usage_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 09:00:00",
            "2026-07-28 10:00:00",
            "2026-07-28 11:00:00",
            "2026-07-28 12:00:00",
        ],

        "Battery_Percentage": [
            100,
            90,
            70,
            50
        ],

        "Charging_Status": [
            False,
            False,
            False,
            False
        ]
    }
)

heavy_hours = behavior.learn_heavy_usage_periods(
    heavy_usage_data
)

run_test(
    "Learn Heavy Usage Periods",
    [10, 11],
    heavy_hours
)

stability_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 09:00:00",
            "2026-07-28 10:00:00",
            "2026-07-28 11:00:00",
            "2026-07-28 12:00:00",
        ],

        "Battery_Percentage": [
            100,
            90,
            80,
            70
        ],

        "Charging_Status": [
            False,
            False,
            False,
            False
        ]
    }
)

stability = behavior.learn_battery_stability(
    stability_data
)

run_test(
    "Learn Battery Stability",
    "Stable",
    stability
)