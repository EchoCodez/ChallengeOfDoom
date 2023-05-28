'''from plyer import notification

notification.notify(
title = "Sample Notification",
message = "This is a sample notification",
timeout = 10
)'''

from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

def test_job():
    print('I am working...')

scheduler = BackgroundScheduler()
job = scheduler.add_job(test_job, 'interval', minutes=1)
scheduler.start()