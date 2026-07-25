class NotificationManager:

    def __init__(self):
        self.last_notifications = {}
        self.history = NotificationHistory()
        print("NotificationHistory initialized")