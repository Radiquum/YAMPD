from . import apiPacks
from flask import request, jsonify
from shared.packs import getPacks, createPack, deletePack


@apiPacks.route("/all", methods=["GET"])
def getPacksEndpoint():
    return jsonify(getPacks())


@apiPacks.route("/new", methods=["POST"])
def createPackEndpoint():
    pack, is_exists = createPack(
        request.json.get("title"),
        request.json.get("author"),
        request.json.get("version"),
        request.json.get("modloader"),
    )

    if is_exists:
        return jsonify({"status": "error", "message": "pack already exists"})

    return jsonify(
        {
            "status": "ok",
            "message": f"pack {pack.title} created",
            "id": pack._id,
        }
    )


@apiPacks.route("/<id>/delete", methods=["GET"])
def deletePackEndpoint(id):
    deletePack(id)
    return jsonify(
        {
            "status": "ok",
            "message": f"pack deleted",
        }
    )
