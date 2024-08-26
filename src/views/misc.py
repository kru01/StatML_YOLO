import json
import os
import random
from pathlib import Path
from time import time

from flask import current_app, jsonify, session
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


static_fd = Path(__file__).parent.parent / "static"

models_fd = static_fd / "models"
md_v10m = YOLO(models_fd / "yolov10m.pt")
md_wildlife = YOLO(models_fd / "last.pt")

store_fd = static_fd / "store"
animal_facts = json.load(open(store_fd / "animal_facts.json"))

img_store_fd = store_fd / "images"


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

    filename = f"{session['uid']}in{model_id}.{img.filename.rsplit('.', 1)[1]}"
    filepath = make_path(filename)

    session[f"in{model_id}"] = f'{current_app.config["IMG_STORE"]}/{filename}'
    img.save(filepath)
    return jsonify({"filename": filename}), 200


def set_names_confs(res, model_id=2):
    names, confs = set(), {}

    for i in range(res.boxes.shape[0]):
        cls = int(res.boxes.cls[i].item())
        name = res.names[cls]
        conf = res.boxes.conf[i].item()

        names.add(name)
        if name not in confs or confs[name] < conf:
            confs[name] = conf

    session[f"out{model_id}_names"] = list(names)
    session[f"out{model_id}_confs"] = confs


def sort_names(names: list, opt=0, confs: dict = None):
    """Sort animals' names based on option.
    :param names: List of animal names to be sorted.
    :param opt: 0 - Alphabet (A-Z), 1 - Confidence (Desc).
    :param confs: Dict of animal predictions and confidences.
    :return: None as names is sorted in-place.
    """
    if opt == 0 or confs is None:
        return names.sort()
    return names.sort(reverse=True, key=lambda name: confs[name])


def get_animal_info(names: list, f_cnt=3, l_cnt=3):
    def get_n_animal_info(name: str, type: str, n: int = 3):
        if len(animal_facts[name][type]) <= n:
            return animal_facts[name][type]
        else:
            idxs = random.sample(range(len(animal_facts[name][type])), n)
            return [animal_facts[name][type][i] for i in idxs]

    facts, links = [], []
    for name in names:
        facts.append(get_n_animal_info(name, "facts", f_cnt))
        links.append(get_n_animal_info(name, "links", l_cnt))

    return [
        {"animal": name, "facts": fact, "links": link}
        for name, fact, link in zip(names, facts, links)
    ]


def rm_expired_imgs(hours=12):
    """Remove all images in static storage that are older than n hours.
    :param hours: Hour limit.
    :return: None.
    """
    print("-- Clearing image storage")
    for item in Path(img_store_fd).glob("*"):
        if "placeholder" in item.name:
            continue
        if item.stat().st_mtime < time() - hours * 3600:  # 1 * 60 * 60
            item.unlink(True)
