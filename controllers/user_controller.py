from flask import request, g
from flask import current_app as app
from flask_restful import Resource
from marshmallow import ValidationError
from Users import UserModel
from schemas.user_schema import userSchema
userModel = UserModel("users.csv")


class UserResource(Resource):

    def get(self, user_id=None):
        app.logger.info(
            f"uuid: {g.uuid}, is_connected: {g.conn["is_connected"]}")
        if user_id is None:
            users = userModel.get_users(user_id=None)
            return userSchema.dump(users, many=True)
        user = userModel.get_users(user_id=user_id)
        if user is None:
            return {"error": "User not found!"}, 404
        return userSchema.dump(user)

    def post(self):
        try:
            data = userSchema.load(request.json)
        except ValidationError as err:
            return {"error": err.messages}, 400
        new_user = userModel.add_user(
            username=data["username"], age=data["age"])
        return new_user, 201, {"location": f"/users/{new_user["user_id"]}"}

    def delete(self, user_id):
        if userModel.delete_user(user_id=user_id):
            return "", 204
        else:
            return {"message": "User not found"}, 404

    def update_user(self, user_id, partial: bool):
        try:
            data = userSchema.load(request.json, partial=partial)
        except ValidationError as err:
            return {"error": err.messages}, 400
        new_username = data["username"] if "username" in data else None
        new_age = data["age"] if "age" in data else None
        updated_user = userModel.update_user(
            user_id=user_id, new_username=new_username, new_age=new_age)
        if updated_user is None:
            return {"error": "User not found!"}, 404
        else:
            return updated_user

    def put(self, user_id):
        return self.update_user(user_id=user_id, partial=False)

    def patch(self, user_id):
        return self.update_user(user_id=user_id, partial=True)
