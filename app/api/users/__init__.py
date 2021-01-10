from flask_restful import Api
from flask import Blueprint

from .resource import User, UserRegister, UserLogin, TokenRefresh, UserLogout

user_bp = Blueprint("user", __name__)
api = Api(user_bp, prefix="/api/v1")


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
