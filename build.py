#!/usr/bin/env python3

import subprocess
import os
import shutil
import argparse


OUT_DIR = "./dist"


parser = argparse.ArgumentParser(
    prog="Yet Another MineCraft ModPack Downloader",
    description="Create and Download mod packs with ease",
    epilog="",
)
parser.add_argument(
    "--no-rebuild",
    help="don't rebuild Next.js frontend",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--exe", help="build an executable files", action="store_true", default=False
)
parser.add_argument(
    "--no-gui", help="ignore the GUI build", action="store_true", default=False
)
parser.add_argument(
    "--no-cli", help="ignore the CLI build", action="store_true", default=False
)


def clearCache():
    if os.path.exists(f"{OUT_DIR}/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/__pycache__")
    if os.path.exists(f"{OUT_DIR}/api/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/api/__pycache__")
    if os.path.exists(f"{OUT_DIR}/api/source/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/api/source/__pycache__")
    if os.path.exists(f"{OUT_DIR}/cli/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/cli/__pycache__")
    if os.path.exists(f"{OUT_DIR}/shared/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/shared/__pycache__")
    if os.path.exists(f"{OUT_DIR}/type/__pycache__"):
        shutil.rmtree(f"{OUT_DIR}/type/__pycache__")


if __name__ == "__main__":
    args = parser.parse_args()

    if os.path.exists(OUT_DIR) and os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)

    os.makedirs(OUT_DIR)

    # TODO: handle multiple package managers line npm(node), deno, yarn
    # TODO?: install node deps automatically

    if not args.no_rebuild:
        build = subprocess.call(["bun", "run", "build"], cwd="./gui", shell=(os.name == "nt"))
        if build != 0:
            print("[ERROR] Next.js gui has failed to build")
            raise

    print("Scanning Next.js out directory...")

    files = [f.name for f in os.scandir("./gui/out") if f.is_file()]
    dirs = [f.name for f in os.scandir("./gui/out") if f.is_dir()]

    os.makedirs(f"{OUT_DIR}/static")
    os.makedirs(f"{OUT_DIR}/templates")

    for file in files:
        if file.endswith(".html"):
            print(f"Copied page: './gui/out/{file}' -> '{OUT_DIR}/templates/{file}'")
            shutil.copyfile(f"./gui/out/{file}", f"{OUT_DIR}/templates/{file}")
            continue
        print(f"Copied asset: './gui/out/{file}' -> '{OUT_DIR}/static/{file}'")
        shutil.copyfile(f"./gui/out/{file}", f"{OUT_DIR}/static/{file}")

    for dir in dirs:
        if dir == "_next":
            print(f"Copied directory: './gui/out/{dir}' -> '{OUT_DIR}/static/{dir}'")
            shutil.copytree(
                f"./gui/out/{dir}", f"{OUT_DIR}/static/{dir}", dirs_exist_ok=True
            )
            continue
        print(f"Copied directory: './gui/out/{dir}' -> '{OUT_DIR}/templates/{dir}'")
        shutil.copytree(
            f"./gui/out/{dir}", f"{OUT_DIR}/templates/{dir}", dirs_exist_ok=True
        )

    print(f"Copied app: './src' -> '{OUT_DIR}'")
    shutil.copytree("./src", f"{OUT_DIR}/", dirs_exist_ok=True)

    print(
        f"Copied requirements.txt: './requirements.txt' -> '{OUT_DIR}/requirements.txt'"
    )
    shutil.copyfile(f"./requirements.txt", f"{OUT_DIR}/requirements.txt")
    clearCache()

    if args.exe and not args.no_gui:
        build = subprocess.call(
            [
                "pyinstaller",
                "main.py",
                "-F",
                "--add-data",
                "static:static",
                "--add-data",
                "templates:templates",
            ],
            cwd="./dist",
            shell=(os.name == "nt"),
        )
        if build != 0:
            print("[ERROR] pyinstaller has failed to build an app")
            raise

        if os.path.exists(f"{OUT_DIR}/dist/main.exe"):
            shutil.move(f"{OUT_DIR}/dist/main.exe", f"{OUT_DIR}/yamcpack.exe")
        elif os.path.exists(f"{OUT_DIR}/dist/main"):
            shutil.move(f"{OUT_DIR}/dist/main", f"{OUT_DIR}/yamcpack")
        else:
            print("[ERROR] no executable found")
            raise

        print("cleanup...")
        shutil.rmtree(f"{OUT_DIR}/dist")
        shutil.rmtree(f"{OUT_DIR}/build")
        os.remove(f"{OUT_DIR}/main.spec")
        clearCache()

    if args.exe and not args.no_cli:
        build = subprocess.call(
            [
                "pyinstaller",
                "cli.py",
                "-F",
                "--add-data",
                "mc_version.json:.",
            ],
            cwd="./dist",
            shell=(os.name == "nt"),
        )
        if build != 0:
            print("[ERROR] pyinstaller has failed to build an app")
            raise

        if os.path.exists(f"{OUT_DIR}/dist/cli.exe"):
            shutil.move(f"{OUT_DIR}/dist/cli.exe", f"{OUT_DIR}/yamcpack-cli.exe")
        elif os.path.exists(f"{OUT_DIR}/dist/cli"):
            shutil.move(f"{OUT_DIR}/dist/cli", f"{OUT_DIR}/yamcpack-cli")
        else:
            print("[ERROR] no executable found")
            raise

        print("cleanup...")
        shutil.rmtree(f"{OUT_DIR}/dist")
        shutil.rmtree(f"{OUT_DIR}/build")
        os.remove(f"{OUT_DIR}/cli.spec")
        clearCache()
