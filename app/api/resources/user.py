from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
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


class UserLogin(Resource):
    def post(self):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_email(user_data.email)

        if user and user.verify_hash(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401


class Users(Resource):
    def get(self):
        return {"users": users_schema.dump(UserModel.find_all())}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
