import os

from flask import Blueprint, current_app, jsonify, request
from ultralytics import YOLO

router = Blueprint("homeRouter", __name__)

ALLOWED_EXTENSIONS = {
    "bmp",
    "dng",
    "jpeg",
    "jpg",
    "mpo",
    "png",
    "tif",
    "tiff",
    "webp",
    "pfm",
}


def is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def make_filepath(filename):
    return os.path.join(
        current_app.static_folder, current_app.config["HOME_STORAGE"], filename
    )


@router.route("/<int:model_id>", methods=["POST"])
def uploadImg(model_id):
    if model_id != 1 and model_id != 2:
        return jsonify({"message": "Invalid model"}), 500

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 500

    img = request.files["file"]

    if img.filename == "":
        return jsonify({"message": "No selected file"}), 500

    if not img or not is_allowed(img.filename):
        return jsonify({"message": "File not supported"}), 500

    filename = f"in{model_id}.{img.filename.rsplit('.', 1)[1]}"
    filepath = make_filepath(filename)

    img.save(filepath)
    return jsonify({"filename": filename}), 200


@router.route("/<int:model_id>", methods=["UPDATE"])
def getInference(model_id):
    if model_id == 1:
        model = "yolov10m.pt"
    elif model_id == 2:
        return jsonify({"message": "Coming soon"}), 500
    else:
        return jsonify({"message": "Invalid model"}), 500

    modelPath = os.path.join(current_app.static_folder, "models", model)
    model = YOLO(modelPath)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "No file part"}), 500

    ext = data["filename"].rsplit(".", 1)[1]
    inFile = f"in{model_id}.{ext}"
    outFile = f"out{model_id}.{ext}"

    inPath = make_filepath(inFile)
    outPath = make_filepath(outFile)

    results = model(inPath)
    results[0].save(outPath)

    return jsonify({"filename": outFile}), 200
