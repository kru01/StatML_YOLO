from flask import Blueprint, current_app, jsonify, render_template, request, session
from shortuuid import uuid

from views.misc import (
    get_animal_info,
    handle_upload_img,
    make_path,
    md_wildlife,
    set_names_confs,
    sort_names,
)

router = Blueprint("wiki", __name__)


@router.route("/wiki")
def wiki():
    if "uid" not in session:
        session["uid"] = uuid()

    d_img = current_app.config["PLHDER_IMG"]
    in2 = session.get("in2", d_img)

    if "out2_names" not in session:
        info = None
    else:
        names = session.get("out2_names", None)
        sort_names(names, 1, session.get("out2_confs", None))
        info = get_animal_info(names)

    return render_template(
        "wiki.html",
        src2=session.get("src2", None),
        out2=session.get("out2", in2),
        info=info,
    )


@router.route("/wiki", methods=["POST"])
def upload_img():
    return handle_upload_img(request, 2)


@router.route("/wiki", methods=["UPDATE"])
def get_inference():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "No file part"}), 500

    ext = data["filename"].rsplit(".", 1)[1]
    inFile = f"{session['uid']}in2.{ext}"
    outFile = f"{session['uid']}out2.{ext}"

    inPath = make_path(inFile)
    outPath = make_path(outFile)

    result = md_wildlife(inPath)[0]
    result.save(outPath)

    set_names_confs(result)
    names = session.get("out2_names", None)
    confs = session.get("out2_confs", None)

    order = request.args.get("order", default=1, type=int)
    sort_names(names, order, confs)

    session[f"src2"] = data["filename"]
    session[f"out2"] = f'{current_app.config["IMG_STORE"]}/{outFile}'
    return jsonify({"filename": outFile, "info": get_animal_info(names)}), 200


@router.route("/wiki/r", methods=["GET"])
def refresh_info():
    if "out2_names" not in session:
        return jsonify({"message": "No inference data"}), 500

    names = session.get("out2_names", None)
    confs = session.get("out2_confs", None)

    order = request.args.get("order", default=1, type=int)
    sort_names(names, order, confs)

    return jsonify({"info": get_animal_info(names)}), 200
