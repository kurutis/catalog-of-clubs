from flask import Blueprint

bp = Blueprint(name="admin", url_prefix="/admin", import_name=__name__)

from . import routes  # noqa: E402
