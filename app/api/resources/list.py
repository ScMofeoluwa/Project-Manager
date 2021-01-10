from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from marshmallow import ValidationError

from ..schema.list import ListSchema
from ..models.list import ListModel

list_schema = ListSchema()
lists_schema = ListSchema(many=True)


class ListCreate(Resource):
    @fresh_jwt_required
    def post(self):
        current_user = get_jwt_identity()
        try:
            list_ = list_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        try:
            list_.user_id = current_user
            list_.save_to_db()
        except:
            return {"message": "Error inserting into database"}, 500

        return list_schema.dump(list_), 201


class List(Resource):
    @jwt_required
    def get(self, list_id):
        current_user = get_jwt_identity()
        list_ = ListModel.find_by_id(list_id)
        if list_ and list_.user_id == current_user:
            return list_schema.dump(list_), 200
        return {"message": "List not found"}, 404

    @fresh_jwt_required
    def delete(self, list_id):
        current_user = get_jwt_identity()
        list_ = ListModel.find_by_id(list_id)
        if list_ and list_.user_id == current_user:
            list_.delete_from_db()
            return {"message": "List deleted"}, 200
        return {"message": "List not found"}, 404

    @fresh_jwt_required
    def patch(self, list_id):
        current_user = get_jwt_identity()
        list_json = request.get_json()
        list_ = ListModel.find_by_id(list_id)

        if list_ and list_.user_id == current_user:
            list_.name = list_json["name"]
            list_.save_to_db()

            return list_schema.dump(list_), 200

        return {"message": "List not found"}, 404


class Lists(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {"lists": lists_schema.dump(ListModel.find_all(current_user))}, 200

