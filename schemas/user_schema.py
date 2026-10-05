from marshmallow import Schema, fields

class UserSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    age = fields.Integer(required=True)


userSchema = UserSchema()