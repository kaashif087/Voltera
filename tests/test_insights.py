from learning.learning_manager import LearningManager
from learning.insights import Insights

manager = LearningManager("tests/test_learning_data.json")
manager.reset_learning_data()

manager.set_value(
    "usage_patterns",
    "active_hours",
    [9, 10, 11]
)

manager.set_value(
    "charging_patterns",
    "usual_charging_hour",
    21
)

manager.set_value(
    "battery_behavior",
    "average_drain_rate",
    10.0
)

manager.set_value(
    "battery_behavior",
    "battery_stability",
    "Stable"
)

manager.set_value(
    "application_usage",
    "most_used_apps",
    {
        "VS Code": 10,
        "Chrome": 5
    }
)

insights = Insights(manager).generate()

print("\n======================================")
print("Insights Test Suite")
print("======================================\n")

for insight in insights:
    print("•", insight)