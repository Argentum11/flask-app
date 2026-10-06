from marshmallow import Schema, fields

class MessageSchema(Schema):
    datadate = fields.String(required=True)
    location = fields.String(required=True)

messageSchema = MessageSchema()