from learning.learning_manager import LearningManager
from learning.charging_patterns import ChargingPatterns


print("\n======================================")
print("Charging Patterns Test Suite")
print("======================================\n")


manager = LearningManager("tests/test_learning_data.json")

manager.reset_learning_data()

charging = ChargingPatterns(manager)

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
    "ChargingPatterns Object Creation",
    True,
    isinstance(charging, ChargingPatterns)
)

import pandas as pd

sample_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 20:00:00",
            "2026-07-28 21:00:00",
            "2026-07-28 21:30:00",
            "2026-07-28 22:00:00",
            "2026-07-28 22:30:00",
        ],

        "Charging_Status": [
            False,
            True,
            True,
            True,
            False
        ],
        "Battery_Percentage": [
    60,
    70,
    80,
    90,
    95
]
    }
)

usual_hour = charging.learn_usual_charging_hour(
    sample_data
)

run_test(
    "Learn Usual Charging Hour",
    21,
    usual_hour
)

average_duration = charging.learn_average_charging_duration(
    sample_data
)

run_test(
    "Learn Average Charging Duration",
    90.0,
    average_duration
)

average_unplug = charging.learn_average_unplug_percentage(
    sample_data
)

run_test(
    "Learn Average Unplug Percentage",
    95.0,
    average_unplug
)

overnight_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 21:30:00",
            "2026-07-28 22:30:00",
            "2026-07-29 02:00:00",
            "2026-07-29 06:30:00",
        ],
        "Charging_Status": [
            False,
            True,
            True,
            False
        ],
        "Battery_Percentage": [
            55,
            60,
            82,
            100
        ]
    }
)

overnight = charging.learn_overnight_charging(
    overnight_data
)

run_test(
    "Learn Overnight Charging",
    True,
    overnight
)