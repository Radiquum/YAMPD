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
parser.add_argument("--no-rebuild", help="don't rebuild Next.js gui", action="store_true", default=False)


if __name__ == "__main__":
    args = parser.parse_args()

    if os.path.exists(OUT_DIR) and os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)

    os.makedirs(OUT_DIR)

    # TODO: handle multiple package managers line npm(node), deno, yarn
    # TODO?: install node deps automatically

    if not args.no_rebuild:
        build = subprocess.call(["bun", "run", "build"], cwd="./gui", shell=True)
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
        print(f"Copied directory: './gui/out/{dir}' -> '{OUT_DIR}/static/{dir}'")
        shutil.copytree(
            f"./gui/out/{dir}", f"{OUT_DIR}/static/{dir}", dirs_exist_ok=True
        )

    print(f"Copied app: './src' -> '{OUT_DIR}'")
    shutil.copytree("./src", f"{OUT_DIR}/", dirs_exist_ok=True)
