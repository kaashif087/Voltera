import pandas as pd

from learning.learning_engine import LearningEngine
from learning.insights import Insights


print("\n======================================")
print("Learning Engine Integration Test")
print("======================================\n")


sample_data = pd.DataFrame(
    {
        "Timestamp": [
            "2026-07-28 09:00:00",
            "2026-07-28 10:00:00",
            "2026-07-28 11:00:00",
            "2026-07-28 21:00:00",
            "2026-07-28 22:00:00",
        ],

        "Battery_Percentage": [
            100,
            90,
            80,
            70,
            90
        ],

        "Charging_Status": [
            False,
            False,
            False,
            False,
            True
        ],

        "CPU_Usage": [
            20,
            35,
            80,
            25,
            15
        ],

        "RAM_Usage": [
            30,
            40,
            70,
            45,
            35
        ],

        "Active_Application": [
            "VS Code",
            "Chrome",
            "VS Code",
            "Spotify",
            "VS Code"
        ]
    }
)


engine = LearningEngine()

engine.learn(sample_data)

print("Learning Engine Executed Successfully")
print("-" * 50)

insights = Insights(engine.manager).generate()

print("Generated Insights\n")

for insight in insights:
    print("•", insight)

print("\nIntegration Test : PASS")