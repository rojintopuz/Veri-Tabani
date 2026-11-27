from flask import Blueprint

doktor_recete_bp = Blueprint("doktor_recete", __name__, url_prefix="/doktor-recete")

from . import routes  # noqa: E402, F401
