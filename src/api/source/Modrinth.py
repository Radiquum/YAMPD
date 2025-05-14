import requests
from config import MODRINTH_UA


def getModrinthMod(slug, version, mod_loader, game_version):
    headers = {"User-Agent": MODRINTH_UA}
    descR = requests.get(f"https://api.modrinth.com/v2/project/{slug}", headers=headers)

    if descR.status_code != 200:
        return {
            "status": "error",
            "message": f"failed to fetch modrinth description: {descR.status_code}",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    versR = requests.get(
        f'https://api.modrinth.com/v2/project/{slug}/version?loaders=["{mod_loader}"]&game_versions=["{game_version}"]',
        headers=headers,
    )

    if versR.status_code != 200:
        return {
            "status": "error",
            "message": f"failed to fetch modrinth mod versions: {versR.status_code}",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    devsR = requests.get(
        f"https://api.modrinth.com/v2/project/{slug}/members",
        headers=headers,
    )

    if devsR.status_code != 200:
        return {
            "status": "error",
            "message": f"failed to fetch modrinth mod developers: {devsR.status_code}",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    desc: dict = descR.json()
    vers: dict = versR.json()
    devs: dict = devsR.json()

    if len(vers) == 0:
        return {
            "status": "error",
            "message": f"mod is not compatible with this game version or mod loader",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    selected_version = vers[0]
    if version:
        for _sf in vers:
            if _sf.get("version_number") == version:
                selected_version = _sf
                break

    primary_file = None
    for _pf in selected_version.get("files"):
        if _pf.get("primary") == True:
            primary_file = _pf
            break

    if primary_file is None:
        return {
            "status": "error",
            "message": f"failed to get primary mod file",
            "slug": slug,
            "version": version,
            "mod_loader": mod_loader,
            "game_version": game_version
        }

    developers = []
    for dev in devs:
        developers.append(dev["user"]["username"])

    isClient = False
    if desc.get("client_side") in ["optional", "required"]:
        isClient = True
    isServer = False
    if desc.get("server_side") in ["optional", "required"]:
        isServer = True

    dependencies = []
    for dep in selected_version.get("dependencies"):
        depDescR = requests.get(f"https://api.modrinth.com/v2/project/{dep.get('project_id')}", headers=headers)
        if depDescR.status_code != 200:
            continue
        depDesc: dict = depDescR.json()
        depMod = getModrinthMod(depDesc.get("slug"), None, mod_loader, game_version)
        dependencies.append(depMod.get("mod"))

    return {
        "status": "ok",
        "mod": {
            "slug": slug,
            "project_id": desc.get("id"),
            "icon": desc.get("icon_url"),
            "title": desc.get("title"),
            "developers": developers,
            "source": "Modrinth",
            "url": f"https://modrinth.com/mod/{slug}",
            "environment": {
                "client": isClient,
                "server": isServer,
            },
            "dependencies": dependencies,
            "file": {
                "version": selected_version.get("version_number"),
                "hashes": primary_file.get("hashes"),
                "url": primary_file.get("url"),
                "filename": primary_file.get("filename"),
                "size": primary_file.get("size"),
            },
        },
    }
