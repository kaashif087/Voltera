from pathlib import Path
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
    "Initial Learning Data",
    {},
    data
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