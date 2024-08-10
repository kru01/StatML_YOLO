import os

from flask import Blueprint, current_app, render_template

bp = Blueprint("views", __name__)


@bp.route("/")
def home():
    return render_template(
        "home.html", imgFile=f'{current_app.config["HOME_STORAGE"]}/placeholder.png'
    )
