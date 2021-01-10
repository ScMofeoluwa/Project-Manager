from flask_restful import Api
from flask import Blueprint

from .user import User, UserRegister, UserLogin, TokenRefresh, UserLogout
from .list import List, Lists, ListCreate
from .task import Task, TaskCreate

api_bp = Blueprint("api", __name__)
api = Api(api_bp, prefix="/api/v1")


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")


api.add_resource(List, "/lists/<int:list_id>")
api.add_resource(Lists, "/lists")
api.add_resource(ListCreate, "/lists/create")


api.add_resource(Task, "/<int:list_id>/tasks/<int:task_id>")
api.add_resource(TaskCreate, "/<int:list_id>/tasks/create")
