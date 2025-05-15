import os
from flask_socketio import emit
import requests
from typing import Literal
from tqdm import tqdm


def download(
    path, url, name, total
) -> tuple[Literal[True], None] | tuple[Literal[False], str]:
    if os.path.exists(f"{path}/{name}"):
        return True, None
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        return False, f"Got a HTTP ERROR {r.status_code} while downloading {name}"

    totalBytes = int(r.headers.get("Content-Length", total))
    if os.getenv("is_cli"):
        with open(f"{path}/{name}", "wb") as fp, tqdm(
            desc=name.ljust(40),
            total=totalBytes,
            miniters=100,
            unit="b",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = fp.write(data)
                bar.update(size)
    else:
        downloaded = 0
        with open(f"{path}/{name}", "wb") as fp:
            for data in r.iter_content(chunk_size=1024):
                size = fp.write(data)
                downloaded += size
                emit(
                    "download_current",
                    {
                        "status": "pending",
                        "total_bytes": totalBytes,
                        "download_bytes": downloaded,
                    },
                    namespace="/",
                    broadcast=True,
                )
    return True, None
