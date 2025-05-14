import json


class ModFile:
    def __init__(
        self, version: str, hashes: dict[str, str], url: str, filename: str, size: int
    ):
        self.version = version
        self.hashes = hashes
        self.url = url
        self.filename = filename
        self.size = size

    def json(self):
        return {
            "version": self.version,
            "hashes": self.hashes,
            "url": self.url,
            "filename": self.filename,
            "size": self.size,
        }
