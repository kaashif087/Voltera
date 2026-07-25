from notification.notification_engine import create_notification
from notification.notification_manager import NotificationManager

print("=" * 60)
print("VOLTERA End-to-End Notification Pipeline Test")
print("=" * 60)

# Create manager
manager = NotificationManager()

# Create notification from recommendation
notification = create_notification("Low Battery Level")

if notification:
    print("✅ Notification created")
else:
    print("❌ Notification creation failed")

# Process notification
result = manager.process(notification)

print("\nManager Result:")
print(result)

print("\nPipeline Test Completed")
print("=" * 60)