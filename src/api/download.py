import os
from . import apiDownload
from flask import request, jsonify, send_file, redirect, url_for, abort
from config import PACKS_FOLDER
import json
from flask_socketio import emit
import requests


def download(path, url, name, total):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        emit(
            "download_current",
            {
                "status": "error",
                "message": f"Got a HTTP ERROR {r.status_code} while downloading {name}",
            },
        )
        return {
            "status": "error",
            "message": f"Got a HTTP ERROR {r.status_code} while downloading {name}",
        }
    downloaded = 0
    if os.path.exists(f"{path}/{name}"):
        emit(
            "download_current",
            {"status": "ok", "message": f"{name} already downloaded"},
            namespace="/",
            broadcast=True,
        )
        return {"status": "ok", "message": f"{name} already downloaded"}
    with open(f"{path}/{name}", "wb") as fp:
        for data in r.iter_content(chunk_size=1024):
            size = fp.write(data)
            downloaded += size
            emit(
                "download_current",
                {
                    "status": "pending",
                    "total_bytes": total,
                    "download_bytes": downloaded,
                },
                namespace="/",
                broadcast=True,
            )
    emit(
        "download_current",
        {"status": "ok", "message": f"{name} downloaded"},
        namespace="/",
        broadcast=True,
    )
    return {
        "status": "ok",
        "message": f"{name} downloaded",
    }


@apiDownload.route("/pack", methods=["POST"])
def downloadPack():
    pack = {}
    pack_id = request.json.get("pack_id")

    with open(f"{PACKS_FOLDER}/{pack_id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()

    mods = pack.get("mods", [])
    total = len(mods)

    os.makedirs(f"{PACKS_FOLDER}/{pack_id}/mods", exist_ok=True)

    for i, mod in enumerate(mods):
        emit(
            "download_total",
            {
                "status": "ok",
                "total": total,
                "current": i,
                "title": mod.get("title"),
                "filename": mod.get("file").get("filename"),
            },
            namespace="/",
            broadcast=True,
        )
        download(
            f"{PACKS_FOLDER}/{pack_id}/mods",
            mod.get("file").get("url"),
            mod.get("file").get("filename"),
            mod.get("file").get("size"),
        )

    emit(
        "download_total",
        {
            "status": "ok",
            "total": total,
            "current": total,
            "title": "",
            "filename": "",
        },
        namespace="/",
        broadcast=True,
    )
    return jsonify(
        {
            "status": "ok",
            "message": f"download of {pack_id} with {total} mods finished",
        },
    )


@apiDownload.route("/mods", methods=["POST"])
def downloadMods():
    pack = {}
    pack_id = request.json.get("pack_id")
    mods_slugs = request.json.get("mods")

    with open(f"{PACKS_FOLDER}/{pack_id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()

    mods = pack.get("mods", [])
    total = len(mods_slugs)

    os.makedirs(f"{PACKS_FOLDER}/{pack_id}/mods", exist_ok=True)

    for i, slug in enumerate(mods_slugs):
        for mod in mods:
            if mod.get("slug") == slug:
                emit(
                    "download_total",
                    {
                        "status": "ok",
                        "total": total,
                        "current": i,
                        "title": mod.get("title"),
                        "filename": mod.get("file").get("filename"),
                    },
                    namespace="/",
                    broadcast=True,
                )
                download(
                    f"{PACKS_FOLDER}/{pack_id}/mods",
                    mod.get("file").get("url"),
                    mod.get("file").get("filename"),
                    mod.get("file").get("size"),
                )

    emit(
        "download_total",
        {
            "status": "ok",
            "total": total,
            "current": total,
            "title": "",
            "filename": "",
        },
        namespace="/",
        broadcast=True,
    )
    return jsonify(
        {
            "status": "ok",
            "message": f"download of {pack_id} with {total} mods finished",
        },
    )
