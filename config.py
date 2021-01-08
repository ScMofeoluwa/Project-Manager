from os import environ, path

from dotenv import load_dotenv

basedir = path.dirname(path.abspath(__file__))
load_dotenv(path.join(basedir, ".env"), verbose=True)


class Config(object):
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    FLASK_TESTING = environ.get("FLASK_TESTING")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_BLACKLIST_ENABLED = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_DEBUG = False
    FLASK_ENV = "production"
