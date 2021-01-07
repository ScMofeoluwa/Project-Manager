from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schema.task import TaskSchema
from ..models.task import TaskModel

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class TaskCreate(Resource):
    def post(self):
        try:
            task = task_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        try:
            task.save_to_db()
        except:
            return {"message": "Error inserting into database"}, 500

        return task_schema.dump(task), 201


class Task(Resource):
    def get(self, task_id):
        task = TaskModel.find_by_id(task_id)
        if task:
            return task_schema.dump(task), 200
        return {"message": "Task not found"}, 404

    def delete(self, task_id):
        task = TaskModel.find_by_id(task_id)
        if task:
            task.delete_from_db()
            return {"message": "Task deleted"}, 200
        return {"message": "Task not found"}, 404


class Tasks(Resource):
    def get(self):
        return {"tasks": tasks_schema.dump(TaskModel.find_all())}, 200
