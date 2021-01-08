from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from config import Config

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["identity"] in BLACKLIST


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .api.resources import api
        api.init_app(app)

        return app
