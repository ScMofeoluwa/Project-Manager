from flask_restful import Api
from flask import Blueprint

from .resource import List, Lists, ListCreate

list_bp = Blueprint("list", __name__)
api = Api(list_bp, prefix="/api/v1")

api.add_resource(List, "/lists/<int:list_id>")
api.add_resource(Lists, "/lists")
api.add_resource(ListCreate, "/lists/create")