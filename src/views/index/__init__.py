from flask import Blueprint

bp = Blueprint(name="index", import_name=__name__)

from . import routes  # noqa: E402
