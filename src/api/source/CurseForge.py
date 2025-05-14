MODLOADER_ENUM = {"forge": 1, "fabric": 4, "quilt": 5, "neoforge": 6}
HASHALGO_ENUM = {1: "sha1", 2: "md5"}

import requests
from config import CURSEFORGE_API_KEY


def getCurseForgeMod(slug, version, mod_loader, game_version):
    headers = {"x-api-key": CURSEFORGE_API_KEY}

    metaR = requests.get(
        f"https://api.curseforge.com/v1/mods/search?gameid=432&slug={slug}",
        headers=headers,
    )
    if metaR.status_code != 200:
        return {
            "status": "error",
            "message": f"failed to fetch curseforge mod: {metaR.status_code}",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    meta: dict = metaR.json()
    if len(meta.get("data")) == 0:
        return {
            "status": "error",
            "message": f"mod not found",
        }
    meta = meta.get("data")[0]

    selected_version = None
    if version:
        versR = requests.get(
            f'https://api.curseforge.com/v1/mods/{meta.get("id")}/files/{version}',
            headers=headers,
        )
    else:
        versR = requests.get(
            f'https://api.curseforge.com/v1/mods/{meta.get("id")}/files?gameVersion={game_version}&modLoaderType={MODLOADER_ENUM[mod_loader]}&pageSize=1',
            headers=headers,
        )

    if versR.status_code != 200:
        return {
            "status": "error",
            "message": f"failed to fetch curseforge mod versions: {versR.status_code}",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    vers: dict = versR.json()
    if len(vers.get("data")) == 0:
        return {
            "status": "error",
            "message": f"mod is not compatible with this game version or mod loader",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    if version:
        selected_version = vers.get("data")
    else:
        selected_version = vers.get("data")[0]

    developers = []
    for dev in meta["authors"]:
        developers.append(dev["name"])

    hashes = {}
    for hash in selected_version.get("hashes"):
        hashes[HASHALGO_ENUM[hash.get("algo")]] = hash.get("value")

    dependencies = []
    for dep in selected_version.get("dependencies"):
        depDescR = requests.get(f"https://api.curseforge.com/v1/mods/{dep.get('modId')}/", headers=headers)
        if depDescR.status_code != 200:
            continue
        depDesc: dict = depDescR.json()
        depMod = getCurseForgeMod(depDesc.get("data").get("slug"), None, mod_loader, game_version)
        dependencies.append(depMod.get("mod"))

    return {
        "status": "ok",
        "mod": {
            "slug": slug,
            "project_id": meta.get("id"),
            "icon": meta.get("logo").get("url"),
            "title": meta.get("name"),
            "developers": developers,
            "source": "CurseForge",
            "url": f"https://www.curseforge.com/minecraft/mc-mods/{slug}",
            "environment": {
                "client": True,
                "server": True,
            },
            "dependencies": dependencies,
            "file": {
                "version": selected_version.get("id"),
                "hashes": hashes,
                "url": selected_version.get("downloadUrl"),
                "filename": selected_version.get("fileName"),
                "size": selected_version.get("fileSizeOnDisk"),
            },
        },
    }
