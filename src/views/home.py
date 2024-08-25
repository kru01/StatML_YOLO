from flask import Blueprint, current_app, jsonify, render_template, request

from views.misc import handle_upload_img, make_path, md_v10m, md_wildlife

router = Blueprint("home", __name__)


@router.route("/")
def home():
    return render_template(
        "home.html", imgFile=f'{current_app.config["IMG_STORE"]}/placeholder.png'
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
    inFile = f"in{model_id}.{ext}"
    outFile = f"out{model_id}.{ext}"

    inPath = make_path(inFile)
    outPath = make_path(outFile)

    results = model(inPath)
    results[0].save(outPath)

    return jsonify({"filename": outFile}), 200
