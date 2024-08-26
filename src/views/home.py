from flask import Blueprint, current_app, jsonify, render_template, request, session
from shortuuid import uuid

from views.misc import (
    handle_upload_img,
    make_path,
    md_v10m,
    md_wildlife,
    set_names_confs,
)

router = Blueprint("home", __name__)


@router.route("/")
def home():
    if "uid" not in session:
        session["uid"] = uuid()

    d_img = current_app.config["PLHDER_IMG"]

    return render_template(
        "home.html",
        src1=session.get("src1", None),
        in1=session.get("in1", d_img),
        out1=session.get("out1", d_img),
        src2=session.get("src2", None),
        in2=session.get("in2", d_img),
        out2=session.get("out2", d_img),
    )


@router.route("/<int:model_id>", methods=["POST"])
def upload_img(model_id):
    return handle_upload_img(request, model_id)


@router.route("/<int:model_id>", methods=["UPDATE"])
def get_inference(model_id):
    if model_id not in {1, 2}:
        return jsonify({"message": "Invalid model"}), 500

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "No file part"}), 500

    if model_id == 1:
        model = md_v10m
    else:
        model = md_wildlife

    ext = data["filename"].rsplit(".", 1)[1]
    inFile = f"{session['uid']}in{model_id}.{ext}"
    outFile = f"{session['uid']}out{model_id}.{ext}"

    inPath = make_path(inFile)
    outPath = make_path(outFile)

    result = model(inPath)[0]
    result.save(outPath)

    if model_id == 2:
        set_names_confs(result)

    session[f"src{model_id}"] = data["filename"]
    session[f"out{model_id}"] = f'{current_app.config["IMG_STORE"]}/{outFile}'
    return jsonify({"filename": outFile}), 200
