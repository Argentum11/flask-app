from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from schemas.message_schema import messageSchema

class MessageResource(Resource):
    def __init__(self):
        self.queue = []
    
    def post(self, user_id):
        try:
            data = messageSchema.load(request.json)
        except ValidationError as err:
            return {"error": err.messages}, 400
        self.queue.append({
            "user_id":user_id,
            "datadate": data["datadate"],
            "location": data["location"]
        })
        print(self.queue)
        return "Acknowledged", 202
        