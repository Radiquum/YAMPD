import os
PACKS_FOLDER = "./packs"
if os.getenv("is_dev") == "True":
    PACKS_FOLDER = "../packs"

IMG_ALLOWED_MIME = {"image/png", "image/jpg", "image/jpeg", "image/webp", "image/jfif"}
