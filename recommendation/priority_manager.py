"""
VOLTERA Recommendation Priority Manager

This module determines the importance of multiple
battery situations and selects the highest priority
recommendation.

Priority Order:

CRITICAL
    ↓
HIGH
    ↓
MEDIUM
    ↓
LOW

Input:
    List of detected battery situations

Output:
    Highest priority situation
"""

PRIORITY_LEVELS = {
    "CRITICAL_BATTERY": 4,
    "RAPID_DRAIN": 3,
    "LOW_BATTERY": 3,
    "HIGH_SYSTEM_LOAD": 2,
    "HIGH_BATTERY_CHARGING": 2,
    "NORMAL_CHARGING": 1,
    "BATTERY_STABLE": 1
}

def select_highest_priority(situations):
    """
    Select the most important situation from a list.

    Args:
        situations (list):
            List of detected battery situations.

    Returns:
        str:
            Highest priority situation.
        None:
            If no situations are provided.
    """

    if not situations:
        return None

    return max(
        situations,
        key=lambda situation: PRIORITY_LEVELS.get(
            situation,
            0
        )
    )

def get_highest_priority_recommendation(situations):
    """
    Select the highest priority situation.

    This function returns the selected situation.
    Recommendation details will be handled by
    recommendation_rules.py.
    """

    return select_highest_priority(situations)