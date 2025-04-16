import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DB_URL = os.environ.get("DB_URL", None)
    ADMIN_AUTH = os.environ.get("ADMIN_AUTH", "").split(",")
    DEV = os.environ.get("DEV", False)
