from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from Users import UserModel
userModel = UserModel("users.csv")


class UserSchema(Schema):
    username = fields.String(required=True)
    age = fields.Integer(required=True)


userSchema = UserSchema()


class UserResource(Resource):

    def get(self, user_id=None):
        if user_id is None:
            return userModel.get_users(user_id=None)
        user = userModel.get_users(user_id=user_id)
        if user is None:
            return {"error": "User not found!"}, 404
        return user

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
