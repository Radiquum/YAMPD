import os
import re
from . import apiPack
from flask import request, jsonify, send_file, redirect, url_for, abort
from config import PACKS_FOLDER, IMG_ALLOWED_MIME
from PIL import Image
from io import BytesIO
import base64
import json


@apiPack.route("/<id>", methods=["GET"])
def getPack(id):
    if not os.path.exists(f"{PACKS_FOLDER}/{id}/packfile.json"):
        return jsonify({"status": "error", "message": "not found"}), 404

    pack = {}
    with open(f"{PACKS_FOLDER}/{id}/packfile.json") as fp:
        pack = json.load(fp)
        pack["_id"] = id
        fp.close()

    return jsonify(pack)


@apiPack.route("/<id>/image", methods=["GET"])
def getPackImage(id):
    if not os.path.exists(f"{PACKS_FOLDER}/{id}/packicon.png"):
        return redirect(url_for("static", filename="defaulticon.png"))

    with open(f"{PACKS_FOLDER}/{id}/packicon.png", mode="rb") as fp:
        f = BytesIO(fp.read())
        return send_file(f, mimetype="image/png")


@apiPack.route("/<id>/image/edit", methods=["POST"])
def editPackImage(id):
    image_string = request.json.get("image")
    image_mime = request.json.get("mimetype")
    if image_string == None:
        return jsonify({"status": "error", "message": "no image provided"})
    if image_mime == None or image_mime not in IMG_ALLOWED_MIME:
        return jsonify({"status": "error", "message": "wrong image format"})

    image_data = base64.b64decode(
        re.sub("^data:image/.+;base64,", "", request.json.get("image"))
    )

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
