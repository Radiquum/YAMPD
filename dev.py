import subprocess
import time
import os

if __name__ == "__main__":

    environment = os.environ.copy()
    environment["is_dev"] = "True"
    environment["NEXT_PUBLIC_API_URL"] = "http://127.0.0.1:5000/api"
    environment["NEXT_PUBLIC_SOCKET_URL"] = "http://127.0.0.1:5000"

    # TODO: handle multiple package managers line npm(node), deno, yarn
    # TODO?: install node deps automatically

    gui_proc = subprocess.Popen(
        ["bun", "run", "dev"], cwd="./gui", env=environment, shell=True
    )
    app_proc = subprocess.Popen(
        ["python", "main.py"], cwd="./src", env=environment, shell=True
    )

    try:
        while gui_proc.poll() is None or app_proc.poll() is None:
            time.sleep(0.1)

    except KeyboardInterrupt:
        gui_proc.terminate()
        app_proc.terminate()
        print("Processes Terminated")
