from flask import request
from flask_restful import Resource
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from .schema import TaskSchema
from .model import TaskModel
from ..lists.model import ListModel

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class TaskCreate(Resource):
    @fresh_jwt_required
    def post(self, list_id):
        current_user = get_jwt_identity()
        list_ = ListModel.find_by_id(list_id)

        if list_.user_id != current_user:
            return {"message": "List not found"}

        try:
            task = task_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        try:
            task.list_id = list_id
            task.save_to_db()
        except:
            return {"message": "Error inserting into database"}, 500

        return task_schema.dump(task), 201


class Task(Resource):
    @jwt_required
    def get(self, list_id, task_id):
        current_user = get_jwt_identity()
        list_ = ListModel.find_by_id(list_id)
        if list_.user_id != current_user:
            return {"message": "List not found"}, 404

        task = TaskModel.find_by_id(task_id)
        if task and task.list_id == list_.id:
            return task_schema.dump(task), 200
        return {"message": "Task not found"}, 404

    @fresh_jwt_required
    def delete(self, list_id, task_id):
        current_user = get_jwt_identity()
        list_ = ListModel.find_by_id(list_id)
        if list_.user_id != current_user:
            return {"message": "List not found"}, 404

        task = TaskModel.find_by_id(task_id)
        if task and task.list_id == list_.id:
            task.delete_from_db()
            return {"message": "Task deleted"}, 200
        return {"message": "Task not found"}, 404

    @fresh_jwt_required
    def patch(self, list_id, task_id):
        current_user = get_jwt_identity()
        task_json = request.get_json()
        list_ = ListModel.find_by_id(list_id)
        if list_.user_id != current_user:
            return {"message": "List not found"}, 404

        task = TaskModel.find_by_id(task_id)
        if task and task.list_id == list_.id:
            task.name = task_json["name"]
            task.save_to_db()

            return task_schema.dump(task)

        return {"message": "Task not found"}, 404
