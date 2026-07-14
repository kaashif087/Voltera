from recommendation.recommendation_rules import get_recommendation_rule


test_situations = [
    "CRITICAL_BATTERY",
    "LOW_BATTERY",
    "RAPID_DRAIN",
    "HIGH_BATTERY_CHARGING",
    "NORMAL_CHARGING",
    "HIGH_SYSTEM_LOAD",
    "BATTERY_STABLE",
    "UNKNOWN_SITUATION"
]


for situation in test_situations:
    result = get_recommendation_rule(situation)

    print("\nSituation:", situation)

    if result:
        print("Priority:", result["priority"])
        print("Title:", result["title"])
        print("Recommendation:", result["recommendation"])
        print("Reason:", result["reason"])
    else:
        print("No recommendation rule found")