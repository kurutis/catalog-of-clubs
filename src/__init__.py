from flask import Flask

from .config import Config
from .db import db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    from .views import index, admin
    app.register_blueprint(index.bp)
    app.register_blueprint(admin.bp)
    if Config.DEV:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
    return app
