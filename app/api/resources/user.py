from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.user import UserModel
from ..schema.user import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRegister(Resource):
    def post(self):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_email(user.email):
            return {"message": "A user with that email already exists"}, 400

        user.password = user.generate_hash(user.password)
        user.save_to_db()

        return {"message": "user created successfully"}, 201


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user_schema.dump(user), 200
        return {"message": "User not found"}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}


class Users(Resource):
    def get(self):
        return {"users": users_schema.dump(UserModel.find_all())}, 200
