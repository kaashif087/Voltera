from notification.notification_manager import NotificationManager
from notification.notification_engine import create_notification

manager = NotificationManager()

recommendations = [
    "Low Battery Level",
    "Predicted Low Battery",
    "Rapid Battery Drain",
    "High System Load",
    "High Battery While Charging",
    "Battery Stable"
]

print("=" * 60)
print("VOLTERA Personalization Integration Test")
print("=" * 60)

for recommendation in recommendations:

    notification = create_notification(recommendation)

    allowed = manager.process(notification)

    print(f"{recommendation:<30} -> {allowed}")