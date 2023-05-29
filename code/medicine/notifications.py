from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler

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

scheduler = BackgroundScheduler()
scheduler.start()
notif = Notification("HALLO", "COOOOOOOL", "10:00", 1)
job = scheduler.add_job(notif.send, 'interval', minutes=notif.increment)

while True:
    pass
