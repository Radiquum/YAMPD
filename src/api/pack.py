import os
import re
from . import apiPack
from flask import request, jsonify, send_file, redirect, url_for
from config import PACKS_FOLDER, IMG_ALLOWED_MIME
from PIL import Image
from io import BytesIO
import base64
from shared.pack import getPack, addMod, deleteMod


@apiPack.route("/<id>", methods=["GET"])
def getPackEndpoint(id):
    pack = getPack(id)
    if pack is None:
        return jsonify({"status": "error", "message": "pack not found"}), 404
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


@apiPack.route("/<id>/mod/add", methods=["POST"])
def addModEndpoint(id):
    source = request.json.get("source", None)
    slug = request.json.get("slug", None)
    version = request.json.get("version", None)
    mod = addMod(id, source, slug, version)

    if mod == "err_404":
        return jsonify({"status": "error", "message": "pack not found"})
    elif mod == "err_source":
        return jsonify({"status": "error", "message": "mod source is required"})
    elif mod == "err_slug":
        return jsonify({"status": "error", "message": "mod slug is required"})
    elif mod == "err_exists":
        return jsonify({"status": "error", "message": "mod already exists"})
    elif isinstance(mod, str):
        return jsonify({"status": "error", "message": mod})

    return jsonify(
        {
            "status": "ok",
            "message": f"mod {mod.get("title")} ({slug}) has been added",
            "mod": mod,
        }
    )


@apiPack.route("/<id>/mod/<slug>/delete", methods=["GET"])
def deleteModEndpoint(id, slug):
    deleteMod(id, slug)
    return jsonify(
        {
            "status": "ok",
            "message": f"mod {slug} has been removed",
        }
    )


# @apiPack.route("/<id>/mods/delete", methods=["POST"])
# def deleteModBulk(id):
#     pack = {}
#     slugs = request.json

#     with open(f"{PACKS_FOLDER}/{id}/packfile.json") as fp:
#         pack = json.load(fp)
#         fp.close()

#     for slug in slugs:
#         for mod in pack.get("mods"):
#             if mod.get("slug") == slug:
#                 pack["mods"].remove(mod)
#                 pack["modpackVersion"] += 1
#                 if os.path.exists(
#                     f"{PACKS_FOLDER}/{id}/mods/{mod.get('file').get('filename')}"
#                 ):
#                     os.remove(
#                         f"{PACKS_FOLDER}/{id}/mods/{mod.get('file').get('filename')}"
#                     )

#     with open(f"{PACKS_FOLDER}/{id}/packfile.json", mode="w", encoding="utf-8") as fp:
#         json.dump(pack, fp)
#         fp.close()

#     return jsonify(
#         {
#             "status": "ok",
#             "message": f"mods has been removed",
#         }
#     )
