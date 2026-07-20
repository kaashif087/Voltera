"""
VOLTERA - Notification Manager

Manages notification delivery by handling:
- Cooldown
- Duplicate suppression
- Priority rules
- Notification processing

Author: VOLTERA
"""

import time

from notification.notification_rules import CRITICAL


class NotificationManager:
    """
    Controls when notifications should be sent.
    """

    def __init__(self):
        """
        Stores recently sent notifications.

        Structure:

        {
            "Low Battery Level": {
                "timestamp": 1721486400,
                "count": 2,
                "last_priority": "HIGH"
            }
        }
        """

        self.last_notifications = {}

    # ---------------------------------------------------------

    def reset(self):
        """
        Clears notification history.
        Useful for testing.
        """

        self.last_notifications.clear()

    # ---------------------------------------------------------

    def is_cooldown_active(self, notification):
        """
        Returns True if cooldown is still active.
        """

        notification_type = notification["type"]
        cooldown = notification["cooldown"]

        # Never seen before
        if notification_type not in self.last_notifications:
            return False

        last_sent = self.last_notifications[notification_type]["timestamp"]

        elapsed = time.time() - last_sent

        return elapsed < cooldown

    # ---------------------------------------------------------

    def can_send(self, notification):
        """
        Determines whether the notification
        should be sent.
        """

        priority = notification["priority"]

        # Critical notifications always go through
        if priority == CRITICAL:
            return True

        if self.is_cooldown_active(notification):
            return False

        return True

    # ---------------------------------------------------------

    def update_history(self, notification):
        """
        Updates notification history.
        """

        notification_type = notification["type"]

        current_time = time.time()

        if notification_type not in self.last_notifications:

            self.last_notifications[notification_type] = {
                "timestamp": current_time,
                "count": 1,
                "last_priority": notification["priority"]
            }

        else:

            self.last_notifications[notification_type]["timestamp"] = current_time
            self.last_notifications[notification_type]["count"] += 1
            self.last_notifications[notification_type]["last_priority"] = notification["priority"]

    # ---------------------------------------------------------

    def process(self, notification):
        """
        Main entry point.

        Returns:
            True  -> Notification allowed
            False -> Notification suppressed
        """

        if notification is None:
            return False

        if not self.can_send(notification):
            return False

        self.update_history(notification)

        return True

    # ---------------------------------------------------------

    def get_history(self):
        """
        Returns in-memory notification history.
        """

        return self.last_notifications