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