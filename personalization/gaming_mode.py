"""
VOLTERA Gaming Mode

Controls notification behavior during gaming sessions.
"""


class GamingMode:
    """
    Handles notification filtering while gaming.
    """

    def __init__(self, enabled: bool):
        self.enabled = enabled

    def is_notification_allowed(self, priority: str) -> bool:
        """
        Returns True if a notification with the given priority
        should be shown during gaming.
        """

        if not self.enabled:
            return True

        priority = priority.upper()

        if priority in ("LOW", "MEDIUM"):
            return False

        return True