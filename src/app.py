from flask import Flask

from routers import home
from views import views

app = Flask(__name__)

app.config["LC_STORAGE"] = "lcStorage"
app.config["HOME_STORAGE"] = f"{app.config['LC_STORAGE']}/home"

app.register_blueprint(views.bp)
app.register_blueprint(home.router)

if __name__ == "__main__":
    app.run(debug=True)
