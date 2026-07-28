import pandas as pd

from learning.learning_manager import LearningManager
from learning.usage_patterns import UsagePatterns

print("\n======================================")
print("Usage Patterns Test Suite")
print("======================================\n")

manager = LearningManager("tests/test_learning_data.json")

manager.reset_learning_data()

usage = UsagePatterns(manager)

def run_test(test_name, expected, actual):
    """
    Display formatted test results.
    """

    print(test_name)
    print(f"Expected : {expected}")
    print(f"Got      : {actual}")

    if expected == actual:
        print("Result   : PASS")
    else:
        print("Result   : FAIL")

    print("-" * 50)

# -------------------------------------------------
# Sample Battery Data
# -------------------------------------------------

sample_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 09:00:00",
            "2026-07-28 09:15:00",
            "2026-07-28 09:30:00",
            "2026-07-28 09:45:00",

            "2026-07-28 10:00:00",
            "2026-07-28 10:15:00",
            "2026-07-28 10:30:00",

            "2026-07-28 11:00:00",
            "2026-07-28 11:15:00",

            "2026-07-28 21:00:00",
        ],

        "Battery_Percentage": [
            100,
            95,
            90,
            85,

            80,
            75,
            70,

            65,
            60,

            50
        ]
    }
)

# -------------------------------------------------
# Test 1 - Learn Active Hours
# -------------------------------------------------

active_hours = usage.learn_active_hours(sample_data)

run_test(
    "Learn Active Hours",
    [9, 10, 11, 21],
    active_hours
)

# -------------------------------------------------
# Test 2 - Learn Idle Hours
# -------------------------------------------------

idle_hours = usage.learn_idle_hours(sample_data)

run_test(
    "Learn Idle Hours",
    [21, 11, 10, 9],
    idle_hours
)

# -------------------------------------------------
# Test 3 - Learn Average Battery By Hour
# -------------------------------------------------

average_battery = usage.learn_average_battery_by_hour(
    sample_data
)

run_test(
    "Learn Average Battery By Hour",
    {
        9: 92.5,
        10: 75.0,
        11: 62.5,
        21: 50.0
    },
    average_battery
)

# -------------------------------------------------
# Test 4 - Learn Weekday Weekend Usage
# -------------------------------------------------

weekday_weekend = usage.learn_weekday_weekend_usage(
    sample_data
)

run_test(
    "Learn Weekday Weekend Usage",
    {
        "weekday_average_usage": 10.0,
        "weekend_average_usage": 0
    },
    weekday_weekend
)