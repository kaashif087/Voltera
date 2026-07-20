from notification.notification_engine import create_notification
from notification.notification_manager import NotificationManager

manager = NotificationManager()

print("=" * 60)
print("VOLTERA Notification Manager Test")
print("=" * 60)

notification = create_notification("Low Battery Level")

print("\nFirst Notification")

print(manager.process(notification))

print(manager.get_history())

print("\nSecond Notification (Immediately)")

print(manager.process(notification))

print(manager.get_history())

print("\nCritical Notification")

critical = create_notification("Critical Battery Level")

print(manager.process(critical))

print(manager.get_history())