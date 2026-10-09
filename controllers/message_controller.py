from flask_restful import Resource
from flask import request, after_this_request
from flask import current_app as app
from marshmallow import ValidationError
from schemas.message_schema import messageSchema


class MessageResource(Resource):
    def __init__(self):
        self.queue = []

    def post(self, user_id):

        @after_this_request
        def set_cookie(response):
            response.set_cookie("sent_messages_before", value="true")
            response.set_cookie("messages_only", value="1", path="/messages")
            return response

        app.logger.info(
            f"Cookies in POST /messages/:user_id : {request.cookies}")
        token = request.headers.get("token")
        if token is None:
            return {}, 401, {"WWW-Authenticate": "A required token must exist."}
        elif self.is_valid_token(token=token):
            try:
                data = messageSchema.load(request.json)
            except ValidationError as err:
                return {"error": err.messages}, 400
            self.queue.append({
                "user_id": user_id,
                "datadate": data["datadate"],
                "location": data["location"]
            })
            print(self.queue)
            return "Acknowledged", 202
        else:
            return {}, 403

    def is_valid_token(self, token):
        return token == "flask"
