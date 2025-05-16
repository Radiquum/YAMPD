import os
import sys
import json

from config import PACKS_FOLDER
from shared.packs import getPacks, createPack, deletePack


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

console = Console()


def getPacksCommand():
    packs = []
    packs_json = getPacks()
    for pack in packs_json:
        packs.append(
            Panel(
                f"[b][cyan]{pack.get('title')}[/cyan][/b]\n{pack.get('author')}\n{len(pack.get('mods'))} mods"
            )
        )
    console.print(Columns(packs))
    exit(0)


def createPackCommand():
    title = prompt("How the mod pack will be named?")
    if title == "":
        console.print("[ERROR]: Pack Title is required!", style="bold red")
        exit(1)
    _id = title.replace(" ", "_")

    if os.path.exists(f"{PACKS_FOLDER}/{_id}"):
        console.print(
            f"Pack {title} already exists in {PACKS_FOLDER}/{_id}", style="green"
        )
        exit(1)
    print(f"Title: {title}")

    author = prompt("Pack author?")
    if author == "":
        console.print("[ERROR]: Pack author is required!", style="bold red")
        exit(1)
    print(f"Author: {author}")

    versions: list = []
    with open(resource_path("./mc_version.json")) as fp:
        versions = json.load(fp)
    versions.reverse()

    print("Game Version")
    game_version = select(
        versions, cursor="🢧", cursor_style="cyan", pagination=True, page_size=10
    )
    print(game_version)

    print("Mod Loader")
    mod_loader = select(
        ["Fabric", "Forge", "Quilt", "NeoForge"], cursor="🢧", cursor_style="cyan"
    )
    print(mod_loader)

    pack, is_exists = createPack(title, author, game_version, mod_loader)
    console.print(
        f"Pack {pack.title} was created in {PACKS_FOLDER}/{pack._id}", style="green"
    )
    exit(0)


def deletePacksCommand():
    packs = []
    packs_json = getPacks()
    for pack in packs_json:
        packs.append(pack.get("title"))
    print("select a pack to delete")
    title = select(
        packs, cursor="🢧", cursor_style="cyan", pagination=True, page_size=10
    )
    _id = title.replace(" ", "_")
    if confirm(f"Are you sure you want to delete pack [cyan]{title}[/cyan]?"):
        deletePack(_id)
        console.print(f"Pack [cyan]{title}[/cyan] was deleted")
    else:
        print("delete cancelled")
    exit(0)
