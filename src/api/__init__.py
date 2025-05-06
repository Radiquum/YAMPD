from flask import Blueprint

apiPack = Blueprint("pack", __name__, url_prefix="/api/pack")
apiPacks = Blueprint("packs", __name__, url_prefix="/api/packs")
apiDownload = Blueprint("download", __name__, url_prefix="/api/download")

from . import pack
from . import packs
from . import download
