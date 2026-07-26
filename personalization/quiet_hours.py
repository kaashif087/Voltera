"""
VOLTERA Quiet Hours

Controls notification behavior during user-defined quiet hours.
"""

from datetime import datetime


class QuietHours:
    """
    Handles notification filtering during quiet hours.
    """

    def __init__(self, enabled: bool, start: str, end: str):
        self.enabled = enabled
        self.start = start
        self.end = end

    def is_quiet_time(self) -> bool:
        """
        Returns True if the current time falls within the configured quiet hours.
        """

        if not self.enabled:
            return False

        now = datetime.now().time()

        start_time = datetime.strptime(self.start, "%H:%M").time()
        end_time = datetime.strptime(self.end, "%H:%M").time()

        # Handles quiet hours crossing midnight
        if start_time <= end_time:
            return start_time <= now <= end_time

        return now >= start_time or now <= end_time

    def is_notification_allowed(self, priority: str) -> bool:
        """
        Returns True if a notification should be shown during quiet hours.
        """

        if not self.is_quiet_time():
            return True

        return priority.upper() == "CRITICAL"