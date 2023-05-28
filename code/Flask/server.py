from flask import Flask, request, jsonify, Response, render_template
from apscheduler.schedulers.background import BackgroundScheduler




app = Flask(__name__)

@app.route("/")
def home():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(test_job, 'interval', minutes=1)
    scheduler.start()
    return "hi"


def test_job():
    print('I am working...')



if __name__ == "__main__":
    app.run(debug=True)


