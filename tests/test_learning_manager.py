from pathlib import Path

learning_file = Path("data/learning_data.json")

if learning_file.exists():
    learning_file.unlink()
import json

from learning.learning_manager import LearningManager


def run_test(test_name, expected, actual):
    """Display formatted test results."""

    print(test_name)
    print(f"Expected : {expected}")
    print(f"Got      : {actual}")

    if expected == actual:
        print("Result   : PASS")
    else:
        print("Result   : FAIL")

    print("-" * 50)


print("\n======================================")
print("Learning Manager Test Suite")
print("======================================\n")

# -------------------------------------------------
# Test 1 - Object Creation
# -------------------------------------------------

manager = LearningManager()

run_test(
    "LearningManager Object Creation",
    True,
    isinstance(manager, LearningManager)
)

# -------------------------------------------------
# Test 2 - File Exists
# -------------------------------------------------

run_test(
    "Learning Database Exists",
    True,
    manager.learning_file.exists()
)

# -------------------------------------------------
# Test 3 - Initial JSON
# -------------------------------------------------

with open(manager.learning_file, "r", encoding="utf-8") as file:
    data = json.load(file)

run_test(
    "Usage Patterns Section Exists",
    True,
    "usage_patterns" in data
)

run_test(
    "Charging Patterns Section Exists",
    True,
    "charging_patterns" in data
)

run_test(
    "Metadata Section Exists",
    True,
    "metadata" in data
)

# -------------------------------------------------
# Test 4 - Save Learning Data
# -------------------------------------------------

manager.learning_data["test"] = "VOLTERA"

manager.save_learning_data()

with open(manager.learning_file, "r", encoding="utf-8") as file:
    saved_data = json.load(file)

run_test(
    "Save Learning Data",
    "VOLTERA",
    saved_data.get("test")
)

# -------------------------------------------------
# Test 5 - Get Value
# -------------------------------------------------

manager.set_value(
    "usage_patterns",
    "active_hours",
    [9, 10, 11]
)

run_test(
    "Get Value",
    [9, 10, 11],
    manager.get_value(
        "usage_patterns",
        "active_hours"
    )
)

# -------------------------------------------------
# Test 6 - Update Section
# -------------------------------------------------

manager.update_section(
    "usage_patterns",
    {
        "active_hours": [8, 9, 10],
        "idle_hours": [2, 3, 4]
    }
)

run_test(
    "Update Section",
    [2, 3, 4],
    manager.get_value(
        "usage_patterns",
        "idle_hours"
    )
)

# -------------------------------------------------
# Test 7 - Reset Learning Data
# -------------------------------------------------

manager.reset_learning_data()

run_test(
    "Reset Learning Data",
    {},
    manager.learning_data["usage_patterns"]
)

run_test(
    "Metadata Reset",
    0,
    manager.learning_data["metadata"]["samples"]
)