import random

from flask import Blueprint, current_app, jsonify, render_template, request

from views.misc import animal_facts, handle_upload_img, make_path, md_wildlife

router = Blueprint("wiki", __name__)

names, confs = set(), {}


def get_names_confs(res):
    global names, confs
    names, confs = set(), {}

    for i in range(res.boxes.shape[0]):
        cls = int(res.boxes.cls[i].item())
        name = res.names[cls]
        conf = res.boxes.conf[i].item()

        names.add(name)
        if name not in confs or confs[name] < conf:
            confs[name] = conf

    names = list(names)


def sort_names(names: list, opt=0, confs: dict = None):
    """Sort animals' names based on option.
    :param names: List of animal names to be sorted.
    :param opt: 0 - Alphabet (A-Z), 1 - Confidence (Desc).
    :param confs: Dict of animal predictions and confidences.
    :return: True if success, Fail otherwise.
    """
    try:
        if opt == 0:
            names.sort()
        else:
            names.sort(reverse=True, key=lambda name: confs[name])
    except:
        return False

    return True


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


@router.route("/wiki")
def wiki():
    return render_template(
        "wiki.html", imgFile=f'{current_app.config["IMG_STORE"]}/placeholder.png'
    )


@router.route("/wiki", methods=["POST"])
def upload_img():
    return handle_upload_img(request, 2)


@router.route("/wiki", methods=["UPDATE"])
def get_inference():
    global names, confs

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "No file part"}), 500

    ext = data["filename"].rsplit(".", 1)[1]
    inFile = f"in2.{ext}"
    outFile = f"out2.{ext}"

    inPath = make_path(inFile)
    outPath = make_path(outFile)

    result = md_wildlife(inPath)[0]
    result.save(outPath)

    get_names_confs(result)
    order = request.args.get("order", default=1, type=int)

    if not sort_names(names, order, confs):
        return jsonify({"message": "Sorting error"}), 500

    return jsonify({"filename": outFile, "info": get_animal_info(names)}), 200
