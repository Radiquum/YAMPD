import os
from . import apiPacks
from flask import request, jsonify
from config import PACKS_FOLDER
import json
import shutil


@apiPacks.route("/all", methods=["GET"])
def getPacks():
    packs = []

    if not os.path.exists(f"{PACKS_FOLDER}"):
        os.makedirs(f"{PACKS_FOLDER}", exist_ok=True)
        return jsonify(packs)

    pack_folders = [f.name for f in os.scandir(PACKS_FOLDER) if f.is_dir()]
    for pack_folder in pack_folders:
        if not os.path.exists(f"{PACKS_FOLDER}/{pack_folder}/packfile.json"):
            continue
        with open(f"{PACKS_FOLDER}/{pack_folder}/packfile.json") as fp:
            pack = json.load(fp)
            pack["_id"] = pack_folder
            packs.append(pack)
            fp.close()
    return jsonify(packs)


@apiPacks.route("/new", methods=["POST"])
def createPack():
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


@apiPacks.route("/<id>/delete", methods=["GET"])
def deletePack(id):
    shutil.rmtree(f"{PACKS_FOLDER}/{id}")
    return jsonify(
        {
            "status": "ok",
            "message": f"pack deleted",
        }
    )
