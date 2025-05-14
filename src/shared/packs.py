import os
from config import PACKS_FOLDER
import json
import shutil

from type.pack import Pack


def getPacks() -> list[Pack]:
    """
    Lists and returns all available packs from PACKS_FOLDER directory defined in config.py
    """
    packs: list[Pack] = []

    if not os.path.exists(f"{PACKS_FOLDER}"):
        os.makedirs(f"{PACKS_FOLDER}", exist_ok=True)
        return packs

    pack_folders = [f.name for f in os.scandir(PACKS_FOLDER) if f.is_dir()]
    for pack_folder in pack_folders:
        if not os.path.exists(f"{PACKS_FOLDER}/{pack_folder}/packfile.json"):
            continue
        with open(f"{PACKS_FOLDER}/{pack_folder}/packfile.json") as fp:
            pack = json.load(fp)
            pack["_id"] = pack_folder
            packs.append(pack)
            fp.close()

    return packs


def createPack(
    title: str, author: str, game_version: str, mod_loader: str
) -> Pack | bool:
    """
    Creates a new pack.
    If pack exists returns tuple[Pack, True], if pack was created returns tuple[Pack, False]
    """
    pack = Pack(
        title.replace(" ", "_"), title, author, game_version, mod_loader, "", [], 0, 0
    )

    if os.path.exists(f"{PACKS_FOLDER}/{pack._id}"):
        return pack, True

    os.makedirs(f"{PACKS_FOLDER}/{pack._id}", exist_ok=True)

    with open(
        os.path.abspath(f"{PACKS_FOLDER}/{pack._id}/packfile.json"),
        mode="w",
        encoding="utf-8",
    ) as fp:
        json.dump(pack.json(), fp)
        fp.close()

    return pack, False


def deletePack(id):
    shutil.rmtree(f"{PACKS_FOLDER}/{id}")
    return True
