from flask_restful import Api
from flask import Blueprint

from .resource import Task, TaskCreate

task_bp = Blueprint("task", __name__)
api = Api(task_bp, prefix="/api/v1")


api.add_resource(Task, "/<int:list_id>/tasks/<int:task_id>")
api.add_resource(TaskCreate, "/<int:list_id>/tasks/create")