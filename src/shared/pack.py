import os
from config import PACKS_FOLDER
import json
from type.pack import Pack
from type.mod import Mod
from typing import Literal
from api.source import Modrinth, CurseForge


def getPack(id: str) -> Pack | None:
    if not os.path.exists(f"{PACKS_FOLDER}/{id}/packfile.json"):
        return None

    pack: Pack = {}
    with open(f"{PACKS_FOLDER}/{id}/packfile.json") as fp:
        pack = json.load(fp)
        pack["_id"] = id
        fp.close()

    return pack


def addMod(
    pack_id: str, source: str, slug: str, version: str | None
) -> (
    Mod
    | Literal["err_404"]
    | Literal["err_source"]
    | Literal["err_slug"]
    | Literal["err_exists"]
    | str
):
    pack: Pack = {}
    mod: Mod = {}

    if not os.path.exists(f"{PACKS_FOLDER}/{pack_id}/packfile.json"):
        return "err_404"
    with open(f"{PACKS_FOLDER}/{pack_id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()
    mod_loader = pack.get("modloader").lower()
    game_version = pack.get("version")

    if not source:
        return "err_source"
    if not slug:
        return "err_slug"

    for mod in pack["mods"]:
        if mod.get("slug") == slug:
            return "err_exists"

    if source == "Modrinth":
        mod = Modrinth.getModrinthMod(slug, version, mod_loader, game_version)
    elif source == "CurseForge":
        mod = CurseForge.getCurseForgeMod(slug, version, mod_loader, game_version)

    if mod.get("status") != "ok":
        return mod.get("message")

    pack["modpackVersion"] += 1
    pack["mods"].append(mod.get("mod"))
    with open(
        f"{PACKS_FOLDER}/{pack_id}/packfile.json", mode="w", encoding="utf-8"
    ) as fp:
        json.dump(pack, fp)
        fp.close()

    return mod.get("mod")


def deleteMod(id: str, slug: str) -> Literal[True]:
    pack = {}
    with open(f"{PACKS_FOLDER}/{id}/packfile.json") as fp:
        pack = json.load(fp)
        fp.close()

    for mod in pack.get("mods"):
        if mod.get("slug") == slug:
            pack["mods"].remove(mod)
            pack["modpackVersion"] += 1
            if os.path.exists(
                f"{PACKS_FOLDER}/{id}/mods/{mod.get('file').get('filename')}"
            ):
                os.remove(f"{PACKS_FOLDER}/{id}/mods/{mod.get('file').get('filename')}")

    with open(f"{PACKS_FOLDER}/{id}/packfile.json", mode="w", encoding="utf-8") as fp:
        json.dump(pack, fp)
        fp.close()

    return True
