import json
import os
from pathlib import Path

from flask import current_app, jsonify
from ultralytics import YOLO

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


staticFolder = Path(__file__).parent.parent / "static"

modelsFolder = staticFolder / "models"
md_v10m = YOLO(modelsFolder / "yolov10m.pt")
md_wildlife = YOLO(modelsFolder / "last.pt")

storeFolder = staticFolder / "store"
animal_facts = json.load(open(storeFolder / "animal_facts.json"))


def is_allowed_ext(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def make_path(filename, type=0):
    """Make path from static_folder to file.
    :param filename: Name of the file.
    :param type: 0 - IMG_STORE, 1 - models.
    :return: Path to the file.
    """
    if type == 0:
        subfolder = current_app.config["IMG_STORE"]
    else:
        subfolder = "models"

    return os.path.join(current_app.static_folder, subfolder, filename)


def handle_upload_img(request, model_id):
    if model_id not in {1, 2}:
        return jsonify({"message": "Invalid model"}), 500

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 500

    img = request.files["file"]

    if img.filename == "":
        return jsonify({"message": "No selected file"}), 500

    if not img or not is_allowed_ext(img.filename):
        return jsonify({"message": "File not supported"}), 500

    filename = f"in{model_id}.{img.filename.rsplit('.', 1)[1]}"
    filepath = make_path(filename)

    img.save(filepath)
    return jsonify({"filename": filename}), 200
