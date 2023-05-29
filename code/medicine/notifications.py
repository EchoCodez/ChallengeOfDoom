from plyer import notification

class Notification():
    def __init__(self, title, message, time, increment=1440):
        self.title = title
        self.message = message
        self.time = time
        self.increment = increment

    def send(self):
        notification.notify(
            title = self.title,
            message = self.message,
        )