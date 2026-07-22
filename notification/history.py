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
                    "Timestamp",
                    "Recommendation",
                    "Priority",
                    "Title",
                    "Message",
                    "Reason",
                    "Status"
                ])

            print("Notification history file created.")

        else:

            print("Notification history file already exists.")