import subprocess
import os
import shutil

OUT_DIR = "./dist"

if __name__ == "__main__":

    if os.path.exists(OUT_DIR) and os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)

    os.makedirs(OUT_DIR)

    subprocess.call(["bun", "run", "build"], cwd="./gui", shell=True)
    files = [f.name for f in os.scandir("./gui/out") if f.is_file()]
    dirs = [f.name for f in os.scandir("./gui/out") if f.is_dir()]

    os.makedirs(f"{OUT_DIR}/static")
    os.makedirs(f"{OUT_DIR}/templates")

    for file in files:
        if file.endswith(".html"):
            shutil.copyfile(f"./gui/out/{file}", f"{OUT_DIR}/templates/{file}")
            continue
        shutil.copyfile(f"./gui/out/{file}", f"{OUT_DIR}/static/{file}")

    for dir in dirs:
        shutil.copytree(f"./gui/out/{dir}", f"{OUT_DIR}/static/{dir}", dirs_exist_ok=True)

    shutil.copytree("./src", f"{OUT_DIR}/", dirs_exist_ok=True)