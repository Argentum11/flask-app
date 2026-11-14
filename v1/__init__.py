from flask import Blueprint
from flask_restful import Api
from v1.controllers.user_controller import UserResource
from v1.controllers.classroom_controller import ClassroomResource
from v1.controllers.message_controller import MessageResource

v1_bp = Blueprint("v1_blueprint", __name__)
api = Api(v1_bp)
api.add_resource(UserResource, "/users", "/users/<int:user_id>")
api.add_resource(ClassroomResource, "/classrooms",
                 "/classrooms/<int:classroom_id>")
api.add_resource(MessageResource, "/messages/<int:user_id>")