from ... import ma
from ..models.list import ListModel
from ..schema.task import TaskSchema


class ListSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)

    class Meta:
        model = ListModel
        load_instance = True
        include_fk = True
