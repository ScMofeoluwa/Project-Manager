from flask_restful import Api

from .user import User, UserRegister, Users, UserLogin, TokenRefresh, UserLogout
from .list import List, Lists, ListCreate, UserLists
from .task import Task, Tasks, TaskCreate

api = Api()

api.add_resource(UserRegister, "/api/register/user")
api.add_resource(User, "/api/users/<int:user_id>")
api.add_resource(Users, "/api/users")
api.add_resource(UserLogin, "/api/auth")
api.add_resource(TokenRefresh, "/api/refresh")
api.add_resource(UserLogout, "/api/logout")


api.add_resource(List, "/api/lists/<int:list_id>")
api.add_resource(Lists, "/api/lists")
api.add_resource(ListCreate, "/api/lists/create")
api.add_resource(UserLists, "/api/users/<int:user_id>/lists")


api.add_resource(Task, "/api/tasks/<int:task_id>")
api.add_resource(Tasks, "/api/tasks")
api.add_resource(TaskCreate, "/api/tasks/create")
