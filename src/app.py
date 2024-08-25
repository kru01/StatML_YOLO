from flask import Flask

from views import home, wiki

app = Flask(__name__)

app.config["STORE"] = "store"
app.config["IMG_STORE"] = f"{app.config['STORE']}/images"

app.register_blueprint(home.router)
app.register_blueprint(wiki.router)

if __name__ == "__main__":
    app.run(debug=True)
