from app import ma
from .model import UserModel
from ..lists.schema import ListSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    lists = ma.Nested(ListSchema, many=True)

    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)
        include_fk = True

