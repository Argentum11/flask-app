from flask import Blueprint, request
from flask_restful import Api
from v2.controllers.user_controller import UserResource

v2_bp = Blueprint("v2_blueprint", __name__)
api = Api(v2_bp)
api.add_resource(UserResource, "/users", "/users/<int:user_id>")


@v2_bp.before_request
def check_token():
    if request.headers.get("Authorization") != "v2-verified":
        return {"error": "Invalid or missing token"}, 401
