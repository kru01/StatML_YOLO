import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from views import home, wiki
from views.misc import rm_expired_imgs

app = Flask(__name__)
app.secret_key = "verysecret"

app.config["STORE"] = "store"
app.config["IMG_STORE"] = f"{app.config['STORE']}/images"
app.config["PLHDER_IMG"] = f"{app.config['IMG_STORE']}/placeholder.png"

app.register_blueprint(home.router)
app.register_blueprint(wiki.router)

sched, hour_limit = BackgroundScheduler(), 6
rm_expired_imgs(hour_limit)

sched.add_job(
    func=lambda: rm_expired_imgs(hour_limit), trigger="interval", hours=hour_limit
)
sched.start()


@atexit.register
def kill_sched():
    sched.shutdown()
    rm_expired_imgs(hour_limit)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
