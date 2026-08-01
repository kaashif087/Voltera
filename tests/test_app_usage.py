from learning.learning_manager import LearningManager
from learning.app_usage import AppUsage

print("\n======================================")
print("Application Usage Test Suite")
print("======================================\n")


manager = LearningManager("tests/test_learning_data.json")
manager.reset_learning_data()

app_usage = AppUsage(manager)


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
    "AppUsage Object Creation",
    True,
    isinstance(app_usage, AppUsage)
)


import pandas as pd

sample_data = pd.DataFrame(
    {
        "Active_Application": [
            "VS Code",
            "Chrome",
            "VS Code",
            "Spotify",
            "VS Code",
            "Chrome"
        ]
    }
)

most_used = app_usage.learn_most_used_apps(
    sample_data
)

run_test(
    "Learn Most Used Applications",
    {
        "VS Code": 3,
        "Chrome": 2,
        "Spotify": 1
    },
    most_used
)

duration_data = pd.DataFrame(
    {
        "Active_Application": [
            "VS Code",
            "Chrome",
            "VS Code",
            "Spotify",
            "VS Code",
            "Chrome"
        ]
    }
)

classification_data = pd.DataFrame(
    {
        "Active_Application": [
            "VS Code",
            "Chrome",
            "Android Studio",
            "Spotify",
            "VS Code",
            "YouTube"
        ]
    }
)

battery_data = pd.DataFrame(
    {
        "Battery_Percentage": [
            100,
            95,
            90,
            80,
            75,
            70
        ],

        "Active_Application": [
            "VS Code",
            "VS Code",
            "Chrome",
            "Chrome",
            "Spotify",
            "Spotify"
        ]
    }
)

# -------------------------------------------------
# Learn App Usage Duration
# -------------------------------------------------

duration = app_usage.learn_app_usage_duration(
    duration_data
)

run_test(
    "Learn App Usage Duration",
    {
        "VS Code": 3,
        "Chrome": 2,
        "Spotify": 1
    },
    duration
)

# -------------------------------------------------
# Work vs Entertainment
# -------------------------------------------------

classification = app_usage.learn_work_vs_entertainment(
    classification_data
)

run_test(
    "Learn Work vs Entertainment",
    {
        "work": 3,
        "entertainment": 3
    },
    classification
)

# -------------------------------------------------
# Battery Intensive Apps
# -------------------------------------------------

battery_apps = app_usage.learn_battery_intensive_apps(
    battery_data
)

run_test(
    "Learn Battery Intensive Apps",
    {
        "Chrome": 7.5,
        "Spotify": 5.0,
        "VS Code": 5.0
    },
    battery_apps
)