from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schema.list import ListSchema
from ..models.list import ListModel

list_schema = ListSchema()
lists_schema = ListSchema(many=True)


class ListCreate(Resource):
    def post(self):
        try:
            list_ = list_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        try:
            list_.save_to_db()
        except:
            return {"message": "Error inserting into database"}, 500

        return list_schema.dump(list_), 201


class List(Resource):
    def get(self, list_id):
        list_ = ListModel.find_by_id(list_id)
        if list_:
            return list_schema.dump(list_), 200
        return {"message": "List not found"}, 404

    def delete(self, list_id):
        list_ = ListModel.find_by_id(list_id)
        if list_:
            list_.delete_from_db()
            return {"message": "List deleted"}, 200
        return {"message": "List not found"}, 404

    def patch(self, list_id):
        list_json = request.get_json()
        list_ = ListModel.find_by_id(list_id)
        if not list_:
            return {"message": "List not found"}, 404

        list_.name = list_json["name"]
        list_.save_to_db()

        return list_schema.dump(list_), 200


class UserLists(Resource):
    def get(self, user_id):
        lists = ListModel.query.filter_by(user_id=user_id)
        return {"lists": lists_schema.dump(lists)}, 200


class Lists(Resource):
    def get(self):
        return {"lists": lists_schema.dump(ListModel.find_all())}, 200
