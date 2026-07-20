"""
VOLTERA - Desktop Notifier

Displays desktop notifications.

Author: VOLTERA
"""

from plyer import notification


class DesktopNotifier:
    """
    Handles desktop notifications.
    """

    APP_NAME = "VOLTERA"

    def send(self, notification_data):
        """
        Sends a desktop notification.

        Parameters:
            notification_data (dict)
        """

        if notification_data is None:
            return False

        notification.notify(
            title=f"{self.APP_NAME} - {notification_data['title']}",
            message=notification_data["message"],
            app_name=self.APP_NAME,
            timeout=8
        )

        return True