import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from recommendation.priority_manager import select_highest_priority


test_cases = [
    (
        ["BATTERY_STABLE", "HIGH_SYSTEM_LOAD", "RAPID_DRAIN"],
        "RAPID_DRAIN"
    ),
    (
        ["LOW_BATTERY", "CRITICAL_BATTERY", "NORMAL_CHARGING"],
        "CRITICAL_BATTERY"
    ),
    (
        ["NORMAL_CHARGING", "BATTERY_STABLE"],
        "NORMAL_CHARGING"
    ),
    (
        [],
        None
    ),
    (
        ["UNKNOWN_SITUATION", "BATTERY_STABLE"],
        "BATTERY_STABLE"
    )
]

for situations, expected in test_cases:

    result = select_highest_priority(situations)

    status = "PASS" if result == expected else "FAIL"

    print(f"\nSituations : {situations}")
    print(f"Expected   : {expected}")
    print(f"Got        : {result}")
    print(f"Result     : {status}")
    print("-" * 50)