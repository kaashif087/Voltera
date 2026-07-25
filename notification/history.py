"""
VOLTERA - Notification History

Responsible for:
- Creating notification history file
- Storing notification records
- Reading notification history
- Supporting future analytics

Author: VOLTERA
"""

import csv
import os

from plyer import notification

class NotificationHistory:
    """
    Manages notification history storage.
    """

    FILE_PATH = "data/notifications.csv"

    def __init__(self):
        """
        Initializes the notification history system.
        """

        self.create_history_file()

    def create_history_file(self):
        """
        Creates the notification history CSV file
        if it does not already exist.
        """

        # Create data folder if missing
        os.makedirs("data", exist_ok=True)

        # Create CSV only if missing
        if not os.path.exists(self.FILE_PATH):

            with open(self.FILE_PATH, "w", newline="", encoding="utf-8") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "recommendation",
                    "priority",
                    "title",
                    "message",
                    "reason",
                    "status"
                ])
            print("Notification history file created.")

        else:

            print("Notification history file already exists.")

    def save(self, notification, status="Sent"):
        """
        Saves a notification to the history CSV.
        """

        with open(self.FILE_PATH, "a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                notification["timestamp"],
                notification["recommendation"],
                notification["priority"],
                notification["title"],
                notification["message"],
                notification["reason"],
                status
            ])

    def load(self):
        """
        Returns all saved notifications.
        """

        with open(self.FILE_PATH, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            return list(reader)