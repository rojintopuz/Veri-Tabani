from flask import Blueprint

doktor_recete_bp = Blueprint("doktor_recete", __name__, url_prefix="/doktor_recete")

from . import routes  # noqa: E402, F401