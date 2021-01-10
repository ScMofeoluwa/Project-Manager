from app import ma
from .model import ListModel
from ..tasks.schema import TaskSchema


class ListSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)

    class Meta:
        model = ListModel
        load_instance = True
        include_fk = True
