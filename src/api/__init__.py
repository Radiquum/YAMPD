from flask import Blueprint

apiPack = Blueprint("pack", __name__, url_prefix="/api/pack")
apiPacks = Blueprint("packs", __name__, url_prefix="/api/packs")

from . import pack
from . import packs
