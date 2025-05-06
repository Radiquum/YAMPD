import os

PACKS_FOLDER = "./packs"
if os.getenv("is_dev") == "True":
    PACKS_FOLDER = "../packs"

IMG_ALLOWED_MIME = {"image/png", "image/jpg", "image/jpeg", "image/webp", "image/jfif"}

MODRINTH_UA = "radiquum/YAMPD (kentai.waah@gmail.com)"
if os.getenv("MODRINTH_UA"):
    MODRINTH_UA = os.getenv("MODRINTH_UA")

CURSEFORGE_API_KEY = "$2a$10$bL4bIL5pUWqfcO7KQtnMReakwtfHbNKh6v1uTpKlzhwoueEJQnPnm"
if os.getenv("CURSEFORGE_API_KEY"):
    CURSEFORGE_API_KEY = os.getenv("CURSEFORGE_API_KEY")
