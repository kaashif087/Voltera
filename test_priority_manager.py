from recommendation.priority_manager import select_highest_priority


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
        "NORMAL_CHARGING",
        "BATTERY_STABLE"
    ],
    [],
    [
        "UNKNOWN_SITUATION",
        "BATTERY_STABLE"
    ]
]


for situations in test_cases:
    result = select_highest_priority(situations)

    print("\nSituations:", situations)
    print("Selected:", result)