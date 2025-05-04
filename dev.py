import subprocess
import time
import os

if __name__ == "__main__":

    environment = os.environ.copy()

    gui_proc = subprocess.Popen(["bun", "run", "dev"], cwd="./gui", shell = True)
    app_proc = subprocess.Popen(["python", "main.py"], cwd="./src", shell = True)

    try:
        while gui_proc.poll() is None or app_proc is None:
            time.sleep(0.1)

    except KeyboardInterrupt:
        gui_proc.terminate()
        app_proc.terminate()
        print("Processed Terminated")