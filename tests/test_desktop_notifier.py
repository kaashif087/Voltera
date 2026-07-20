from notification.notification_engine import create_notification
from notification.desktop_notifier import DesktopNotifier

notifier = DesktopNotifier()

notification = create_notification("Critical Battery Level")

print("Sending notification...")

notifier.send(notification)

print("Done.")
