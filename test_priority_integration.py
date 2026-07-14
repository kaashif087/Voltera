from recommendation.priority_manager import (
    get_highest_priority_recommendation
)

from recommendation.recommendation_rules import (
    get_recommendation_rule
)


test_cases = [
    [
        "BATTERY_STABLE",
        "HIGH_SYSTEM_LOAD",
        "RAPID_DRAIN"
    ],

    [
        "LOW_BATTERY",
        "CRITICAL_BATTERY",
        "NORMAL_CHARGING"
    ],

    [
        "HIGH_BATTERY_CHARGING",
        "NORMAL_CHARGING"
    ]
]


for situations in test_cases:

    selected = get_highest_priority_recommendation(
        situations
    )

    recommendation = get_recommendation_rule(
        selected
    )

    print("\nDetected Situations:")
    print(situations)

    print("Selected Situation:")
    print(selected)

    print("Recommendation:")
    print(recommendation["recommendation"])