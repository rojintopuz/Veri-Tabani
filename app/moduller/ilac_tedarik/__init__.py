from flask import Blueprint

ilac_tedarik_bp = Blueprint("ilac_tedarik", __name__, url_prefix="/ilac-tedarik")

from . import routes  # noqa: E402, F401
