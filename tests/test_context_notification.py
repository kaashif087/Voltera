from notification.recommendation_adapter import (
    adapt_recommendation
)

from notification.notification_engine import (
    create_notification
)

from notification.notification_manager import (
    NotificationManager
)


def test_recommendation_to_notification():
    recommendation = {
        "situation": "LOW_BATTERY",
        "priority": "HIGH",
        "title": "Low Battery Level",
        "recommendation": (
            "Consider charging your device."
        ),
        "reason": "Battery level is low."
    }

    notification_name = adapt_recommendation(
        recommendation
    )

    assert notification_name == "Low Battery Level"

    notification = create_notification(
        notification_name
    )

    assert notification is not None
    assert notification["type"] == "Low Battery Level"
    assert notification["priority"] == "HIGH"


def test_notification_manager_processing():
    recommendation = {
        "situation": "CRITICAL_BATTERY",
        "priority": "CRITICAL",
        "title": "Critical Battery Level",
        "recommendation": (
            "Connect your charger immediately."
        ),
        "reason": "Battery is critically low."
    }

    notification_name = adapt_recommendation(
        recommendation
    )

    notification = create_notification(
        notification_name
    )

    manager = NotificationManager()

    manager.reset()

    result = manager.process(notification)

    assert result is True


def test_unknown_recommendation_does_not_notify():
    recommendation = {
        "situation": "UNKNOWN_SITUATION",
        "priority": "LOW"
    }

    notification_name = adapt_recommendation(
        recommendation
    )

    assert notification_name is None

    notification = create_notification(
        notification_name
    )

    assert notification is None


def test_notification_contains_required_fields():
    recommendation = {
        "situation": "HIGH_SYSTEM_LOAD",
        "priority": "MEDIUM"
    }

    notification_name = adapt_recommendation(
        recommendation
    )

    notification = create_notification(
        notification_name
    )

    assert notification is not None

    required_fields = {
        "title",
        "message",
        "priority",
        "type",
        "timestamp",
        "recommendation",
        "reason",
        "cooldown"
    }

    assert required_fields.issubset(
        notification.keys()
    )


if __name__ == "__main__":

    tests = [
        (
            "Recommendation To Notification",
            test_recommendation_to_notification
        ),
        (
            "Notification Manager Processing",
            test_notification_manager_processing
        ),
        (
            "Unknown Recommendation",
            test_unknown_recommendation_does_not_notify
        ),
        (
            "Notification Required Fields",
            test_notification_contains_required_fields
        ),
    ]

    passed = 0

    print("\nContext Notification Integration Tests")
    print("=" * 50)

    for name, test in tests:

        try:
            test()
            print(f"{name:<38} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<38} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 50)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL CONTEXT NOTIFICATION TESTS PASSED")
    else:
        print("SOME CONTEXT NOTIFICATION TESTS FAILED")