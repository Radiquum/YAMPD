import json
from .mod import Mod


class Pack:
    def __init__(
        self,
        _id: str,
        title: str,
        author: str,
        version: str,
        modloader: str,
        updateURL: str,
        mods: list[Mod],
        modpackVersion: int = 0,
        formatVersion: int = 0,
    ):
        self._id = _id
        self.title = title
        self.author = author
        self.version = version
        self.modloader = modloader
        self.updateURL = updateURL
        self.mods = mods
        self.modpackVersion = modpackVersion
        self.formatVersion = formatVersion

    def json(self):
        return {
            "title": self.title,
            "author": self.author,
            "version": self.version,
            "modloader": self.modloader,
            "updateURL": self.updateURL,
            "mods": self.mods,
            "modpackVersion": self.modpackVersion,
            "formatVersion": self.formatVersion,
        }
