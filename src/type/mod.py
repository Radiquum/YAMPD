import json
from .file import ModFile


class Mod:
    def __init__(
        self,
        slug: str,
        project_id: str,
        icon: str,
        title: str,
        developers: list[str],
        source: str,
        environment: dict[str, bool],
        dependencies: list,
        file: ModFile,
    ):
        self.slug = slug
        self.project_id = project_id
        self.icon = icon
        self.title = title
        self.developers = developers
        self.source = source
        self.environment = environment
        self.dependencies = dependencies
        self.file = file

    def json(self):
        return {
            "slug": self.slug,
            "project_id": self.project_id,
            "icon": self.icon,
            "title": self.title,
            "developers": self.developers,
            "source": self.source,
            "environment": self.environment,
            "dependencies": self.dependencies,
            "file": self.file,
        }
