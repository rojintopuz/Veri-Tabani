from flask import Blueprint

eczane_satis_bp = Blueprint("eczane_satis", __name__, url_prefix="/eczane-satis")

from . import routes  # noqa: E402, F401