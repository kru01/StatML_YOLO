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


def make_path(filename, type=0):
    """Make path from static_folder to file.
    :param filename: Name of the file.
    :param type: 0 - HOME_STORAGE, 1 - models.
    :return: Path to the file.
    """
    if type == 0:
        subfolder = current_app.config["HOME_STORAGE"]
    else:
        subfolder = "models"

    return os.path.join(current_app.static_folder, subfolder, filename)


@router.route("/<int:model_id>", methods=["POST"])
def uploadImg(model_id):
    if model_id not in {1, 2}:
        return jsonify({"message": "Invalid model"}), 500

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 500

    img = request.files["file"]

    if img.filename == "":
        return jsonify({"message": "No selected file"}), 500

    if not img or not is_allowed(img.filename):
        return jsonify({"message": "File not supported"}), 500

    filename = f"in{model_id}.{img.filename.rsplit('.', 1)[1]}"
    filepath = make_path(filename)

    img.save(filepath)
    return jsonify({"filename": filename}), 200


@router.route("/<int:model_id>", methods=["UPDATE"])
def getInference(model_id):
    if model_id not in {1, 2}:
        return jsonify({"message": "Invalid model"}), 500

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "No file part"}), 500

    try:
        if model_id == 1:
            model = getInference.md_v10m
        else:
            model = getInference.md_wildlife
    except AttributeError:
        getInference.md_v10m = YOLO(make_path("yolov10m.pt", 1))
        getInference.md_wildlife = YOLO(make_path("last.pt", 1))

        if model_id == 1:
            model = getInference.md_v10m
        else:
            model = getInference.md_wildlife

    ext = data["filename"].rsplit(".", 1)[1]
    inFile = f"in{model_id}.{ext}"
    outFile = f"out{model_id}.{ext}"

    inPath = make_path(inFile)
    outPath = make_path(outFile)

    results = model(inPath)
    results[0].save(outPath)

    return jsonify({"filename": outFile}), 200
