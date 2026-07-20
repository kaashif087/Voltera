"""
VOLTERA - Notification Engine

This module converts Recommendation Engine outputs into
standardized notification objects.

Responsibilities:
- Validate recommendations
- Create notification objects
- Generate timestamps
- Return standardized notification data

Author: VOLTERA
"""

from datetime import datetime

from notification.notification_rules import (
    get_notification_rule,
    is_valid_recommendation
)


def create_notification(recommendation):
    """
    Creates a notification object from a recommendation.

    Parameters:
        recommendation (str)

    Returns:
        dict or None
    """

    if not is_valid_recommendation(recommendation):
        return None

    rule = get_notification_rule(recommendation)

    notification = {
        "title": rule["title"],
        "message": rule["message"],
        "priority": rule["priority"],
        "type": recommendation,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recommendation": recommendation,
        "reason": "Generated from Recommendation Engine",
        "cooldown": rule["cooldown"]
    }

    return notification


def display_notification(notification):
    """
    Displays a notification in the console.

    This is only for testing.
    Future versions will use desktop notifications.
    """

    if notification is None:
        print("\nNo notification generated.")
        return

    print("\n" + "=" * 60)
    print("VOLTERA NOTIFICATION")
    print("=" * 60)

    print(f"Title          : {notification['title']}")
    print(f"Message        : {notification['message']}")
    print(f"Priority       : {notification['priority']}")
    print(f"Type           : {notification['type']}")
    print(f"Timestamp      : {notification['timestamp']}")
    print(f"Recommendation : {notification['recommendation']}")
    print(f"Reason         : {notification['reason']}")
    print(f"Cooldown       : {notification['cooldown']} seconds")

    print("=" * 60)


if __name__ == "__main__":

    print("=" * 60)
    print("VOLTERA Notification Engine Test")
    print("=" * 60)

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

        print(f"\nRecommendation: {recommendation}")

        notification = create_notification(recommendation)

        display_notification(notification)