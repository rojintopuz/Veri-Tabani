from flask import Blueprint

hasta_muayene_bp = Blueprint("hasta_muayene", __name__, url_prefix="/hasta-muayene")

from . import routes  # noqa: E402, F401