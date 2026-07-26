"""
VOLTERA Preference Rules

Determines whether notifications should be shown
based on user preferences.
"""

from personalization.user_profile import UserProfile


class PreferenceRules:
    """
    Applies user preference rules.
    """

    def __init__(self, profile: UserProfile):
        self.profile = profile

    def is_battery_notification_allowed(self, battery_percentage: int) -> bool:
        """
        Returns True if the battery notification
        should be shown.
        """

        return battery_percentage <= self.profile.battery_threshold

    def is_charging_notification_allowed(self) -> bool:
        """
        Returns True if charging notifications are enabled.
        """

        return self.profile.charging_notification_level > 0

    def is_prediction_notification_allowed(self) -> bool:
        """
        Returns True if prediction alerts are enabled.
        """

        return self.profile.prediction_alerts

    def is_rapid_drain_notification_allowed(self) -> bool:
        """
        Returns True if rapid battery drain alerts are enabled.
        """

        return self.profile.rapid_drain_alerts

    def is_system_load_notification_allowed(self) -> bool:
        """
        Returns True if high system load alerts are enabled.
        """

        return self.profile.high_system_load_alerts