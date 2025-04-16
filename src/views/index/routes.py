from flask import render_template
from src.views.index import bp
from src import db

@bp.route("/")
def index():
    return render_template("index.html", coteries=db.get_coteries(), types=db.get_types(),
                           addresses=db.get_addresses())