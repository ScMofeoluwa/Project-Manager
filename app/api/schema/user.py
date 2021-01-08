from ... import ma
from ..models.user import UserModel
from ..schema.list import ListSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    lists = ma.Nested(ListSchema, many=True)

    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)
        dump_only = ("username",)
        include_fk = True

