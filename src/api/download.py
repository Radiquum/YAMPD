import os
from . import apiDownload
from flask import request, jsonify
from config import PACKS_FOLDER
import json
from flask_socketio import emit

from shared.download import download


@apiDownload.route("/pack", methods=["POST"])
def downloadPackEndpoint():
    pack = {}
    pack_id = request.json.get("pack_id")

    with open(f"{PACKS_FOLDER}/{pack_id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()

    mods = pack.get("mods", [])
    queue = []
    for mod in mods:
        queue.append(
            {
                "slug": mod.get("slug"),
                "title": mod.get("file").get("title"),
                "url": mod.get("file").get("url"),
                "filename": mod.get("file").get("filename"),
                "size": mod.get("file").get("size"),
            }
        )
        for dep in mod.get("dependencies"):
            queue.append(
                {
                    "slug": dep.get("slug"),
                    "title": dep.get("file").get("title"),
                    "url": dep.get("file").get("url"),
                    "filename": dep.get("file").get("filename"),
                    "size": dep.get("file").get("size"),
                }
            )
    queue = list({mod["slug"]: mod for mod in queue}.values())
    total = len(queue)

    os.makedirs(f"{PACKS_FOLDER}/{pack_id}/mods", exist_ok=True)

    for i, mod in enumerate(queue):
        emit(
            "download_total",
            {
                "status": "ok",
                "total": total,
                "current": i,
                "title": mod.get("title"),
                "filename": mod.get("filename"),
            },
            namespace="/",
            broadcast=True,
        )
        status, message = download(
            f"{PACKS_FOLDER}/{pack_id}/mods",
            mod.get("url"),
            mod.get("filename"),
            mod.get("size"),
        )
        if status is False:
            emit(
                "download_current",
                {
                    "status": "error",
                    "message": message,
                },
                namespace="/",
                broadcast=True,
            )
        else:
            emit(
                "download_current",
                {
                    "status": "ok",
                    "message": mod.get("filename"),
                },
                namespace="/",
                broadcast=True,
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
def downloadModsEndpoint():
    pack = {}
    pack_id = request.json.get("pack_id")
    mods_slugs = request.json.get("mods")

    with open(f"{PACKS_FOLDER}/{pack_id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()

    mods = pack.get("mods", [])
    queue = []
    for slug in mods_slugs:
        for mod in mods:
            if mod.get("slug") == slug:
                queue.append(
                    {
                        "slug": mod.get("slug"),
                        "title": mod.get("file").get("title"),
                        "url": mod.get("file").get("url"),
                        "filename": mod.get("file").get("filename"),
                        "size": mod.get("file").get("size"),
                    }
                )
                for dep in mod.get("dependencies"):
                    queue.append(
                        {
                            "slug": dep.get("slug"),
                            "title": dep.get("file").get("title"),
                            "url": dep.get("file").get("url"),
                            "filename": dep.get("file").get("filename"),
                            "size": dep.get("file").get("size"),
                        }
                    )
    queue = list({mod["slug"]: mod for mod in queue}.values())
    total = len(queue)

    os.makedirs(f"{PACKS_FOLDER}/{pack_id}/mods", exist_ok=True)

    for i, mod in enumerate(queue):
        emit(
            "download_total",
            {
                "status": "ok",
                "total": total,
                "current": i,
                "title": mod.get("title"),
                "filename": mod.get("filename"),
            },
            namespace="/",
            broadcast=True,
        )
        status, message = download(
            f"{PACKS_FOLDER}/{pack_id}/mods",
            mod.get("url"),
            mod.get("filename"),
            mod.get("size"),
        )
        if status is False:
            emit(
                "download_current",
                {
                    "status": "error",
                    "message": message,
                },
                namespace="/",
                broadcast=True,
            )
        else:
            emit(
                "download_current",
                {
                    "status": "ok",
                    "message": mod.get("filename"),
                },
                namespace="/",
                broadcast=True,
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
            "message": f"download of {total} mods finished",
        },
    )
