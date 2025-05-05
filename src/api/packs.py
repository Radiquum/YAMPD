import os
from . import apiPacks
from flask import request, jsonify
from config import PACKS_FOLDER
import json


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
