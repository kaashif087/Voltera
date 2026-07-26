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

from notification.history import NotificationHistory
from notification.notification_rules import CRITICAL

from personalization.preference_manager import PreferenceManager
from personalization.preference_rules import PreferenceRules
from personalization.gaming_mode import GamingMode
from personalization.quiet_hours import QuietHours


print("Loading Notification Manager...")
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

        # Persistent notification history
        self.history = NotificationHistory()

        print("NotificationHistory initialized")

                # Load user preferences
        self.preference_manager = PreferenceManager()
        self.profile = self.preference_manager.load_preferences()

        # Initialize personalization modules
        self.preference_rules = PreferenceRules(self.profile)

        self.gaming_mode = GamingMode(
            enabled=self.profile.gaming_mode
        )

        self.quiet_hours = QuietHours(
            enabled=self.profile.quiet_hours_enabled,
            start=self.profile.quiet_start,
            end=self.profile.quiet_end
        )

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

    def passes_personalization(self, notification):
        """
        Determines whether the notification should be sent
        according to user preferences.
        """

        notification_type = notification["type"]
        priority = notification["priority"]

        # -----------------------------
        # Battery Notifications
        # -----------------------------
        if notification_type == "Low Battery Level":
            battery = notification.get("battery_percentage", 0)

            if not self.preference_rules.is_battery_notification_allowed(battery):
                return False

        # -----------------------------
        # Prediction Alerts
        # -----------------------------
        elif notification_type in (
            "Predicted Low Battery",
            "Predicted Critical Battery"
        ):
            if not self.preference_rules.is_prediction_notification_allowed():
                return False

        # -----------------------------
        # Rapid Drain
        # -----------------------------
        elif notification_type == "Rapid Battery Drain":
            if not self.preference_rules.is_rapid_drain_notification_allowed():
                return False

        # -----------------------------
        # High System Load
        # -----------------------------
        elif notification_type == "High System Load":
            if not self.preference_rules.is_system_load_notification_allowed():
                return False

        # -----------------------------
        # Charging Notifications
        # -----------------------------
        elif notification_type in (
            "High Battery While Charging",
            "Charging Normally"
        ):
            if not self.preference_rules.is_charging_notification_allowed():
                return False

        # -----------------------------
        # Gaming Mode
        # -----------------------------
        if not self.gaming_mode.is_notification_allowed(priority):
            return False

        # -----------------------------
        # Quiet Hours
        # -----------------------------
        if not self.quiet_hours.is_notification_allowed(priority):
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

        if notification is None:
            return False

        if not self.passes_personalization(notification):
            return False

        if not self.can_send(notification):
            return False

        self.update_history(notification)

        self.history.save(notification)

        return True

    # ---------------------------------------------------------

    def get_history(self):
        """
        Returns in-memory notification history.
        """

        return self.last_notifications