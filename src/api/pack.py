import os
import re
from . import api
from flask import request, jsonify
from config import PACKS_FOLDER, IMG_ALLOWED_MIME
import json
from PIL import Image
from io import BytesIO
import base64

@api.route("/new", methods=["POST"])
def APIPackNew():
    pack = {
        "formatVersion": 0,
        "modpackVersion": 0,
        "title": request.json.get("title"),
        "author": request.json.get("author"),
        "version": request.json.get("version"),
        "modloader": request.json.get("modloader"),
        "updateURL": "",
        "mods": [],
    }
    title = pack.get("title").replace(" ", "_")

    if os.path.exists(f"{PACKS_FOLDER}/{title}"):
        return jsonify({"status": "error", "message": "pack already exists"})

    os.makedirs(f"{PACKS_FOLDER}/{title}", exist_ok=True)

    with open(
        os.path.abspath(f"{PACKS_FOLDER}/{title}/packfile.json"),
        mode="w",
        encoding="utf-8",
    ) as fp:
        json.dump(pack, fp)
        fp.close()

    return jsonify(
        {
            "status": "ok",
            "message": f"pack {pack.get('title')} created",
            "id": title,
        }
    )


@api.route("/<id>/image/edit", methods=["POST"])
def APIPackImageEdit(id):

    image_string = request.json.get("image")
    image_mime = request.json.get("mimetype")
    if image_string == None:
        return jsonify({"status": "error", "message": "no image provided"})
    if image_mime == None or image_mime not in IMG_ALLOWED_MIME:
        return jsonify({"status": "error", "message": "wrong image format"})

    image_data = base64.b64decode(re.sub("^data:image/.+;base64,", "", request.json.get("image")))

    image = Image.open(BytesIO(image_data))
    image = image.resize((512, 512), Image.Resampling.LANCZOS)
    image.save(
        f"{PACKS_FOLDER}/{id}/packicon.png",
        "png",
    )

    return jsonify(
        {
            "status": "ok",
            "message": "image updated",
        }
    )
