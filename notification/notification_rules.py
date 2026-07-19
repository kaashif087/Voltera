"""
VOLTERA - Notification Rules

This module defines notification priorities and maps
Recommendation Engine outputs to notification metadata.

Responsibilities:
- Define notification priorities
- Store notification rules
- Validate recommendations
- Return notification rules

Author: VOLTERA
"""

# ==========================================================
# Notification Priorities
# ==========================================================

CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"


# ==========================================================
# Notification Rules
# ==========================================================

NOTIFICATION_RULES = {

    "Critical Battery Level": {
        "priority": CRITICAL,
        "title": "Critical Battery",
        "message": "Battery is critically low. Connect your charger immediately.",
        "cooldown": 0
    },

    "Low Battery Level": {
        "priority": HIGH,
        "title": "Low Battery",
        "message": "Battery is running low. Please charge your device soon.",
        "cooldown": 900  # 15 minutes
    },

    "Predicted Critical Battery": {
        "priority": CRITICAL,
        "title": "Battery Prediction",
        "message": "Battery is predicted to become critically low soon.",
        "cooldown": 300  # 5 minutes
    },

    "Predicted Low Battery": {
        "priority": HIGH,
        "title": "Battery Prediction",
        "message": "Battery is predicted to become low soon.",
        "cooldown": 600  # 10 minutes
    },

    "Rapid Battery Drain": {
        "priority": HIGH,
        "title": "Rapid Battery Drain",
        "message": "Battery is draining faster than expected.",
        "cooldown": 300  # 5 minutes
    },

    "High System Load": {
        "priority": MEDIUM,
        "title": "High System Load",
        "message": "High CPU or RAM usage is affecting battery life.",
        "cooldown": 600  # 10 minutes
    },

    "High Battery While Charging": {
        "priority": MEDIUM,
        "title": "Battery Charged",
        "message": "Battery is highly charged. Consider unplugging the charger.",
        "cooldown": 1800  # 30 minutes
    },

    "Charging Normally": {
        "priority": LOW,
        "title": "Charging",
        "message": "Battery is charging normally.",
        "cooldown": 1800  # 30 minutes
    },

    "Battery Stable": {
        "priority": LOW,
        "title": "Battery Stable",
        "message": "Battery condition is stable.",
        "cooldown": 3600  # 1 hour
    }
}


# ==========================================================
# Functions
# ==========================================================

def get_notification_rule(recommendation):
    """
    Returns the notification rule for the given recommendation.

    Parameters:
        recommendation (str): Recommendation from the Recommendation Engine

    Returns:
        dict or None:
            Notification rule if found,
            otherwise None.
    """
    return NOTIFICATION_RULES.get(recommendation)


def is_valid_recommendation(recommendation):
    """
    Checks whether a recommendation has a notification rule.

    Parameters:
        recommendation (str)

    Returns:
        bool
    """
    return recommendation in NOTIFICATION_RULES


def get_all_notification_rules():
    """
    Returns all notification rules.

    Useful for debugging, testing,
    and future admin dashboards.
    """
    return NOTIFICATION_RULES


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("VOLTERA Notification Rules Test")
    print("=" * 50)

    recommendations = [
        "Critical Battery Level",
        "Low Battery Level",
        "Predicted Critical Battery",
        "Predicted Low Battery",
        "Rapid Battery Drain",
        "High System Load",
        "High Battery While Charging",
        "Charging Normally",
        "Battery Stable",
        "Unknown Recommendation"
    ]

    for recommendation in recommendations:

        print(f"\nRecommendation : {recommendation}")

        if is_valid_recommendation(recommendation):
            rule = get_notification_rule(recommendation)

            print(f"Priority       : {rule['priority']}")
            print(f"Title          : {rule['title']}")
            print(f"Message        : {rule['message']}")
            print(f"Cooldown       : {rule['cooldown']} seconds")

        else:
            print("No notification rule found.")