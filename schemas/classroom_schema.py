from marshmallow import Schema, fields, pre_dump
from schemas.user_schema import UserSchema

class ClassroomSchema(Schema):
    class_id = fields.Integer(dump_only=True)
    class_name = fields.String(required=True)
    students = fields.List(fields.Nested(UserSchema), required=True)
    student_count = fields.Integer(dump_only=True)

    @pre_dump
    def add_student_count(self, data, **kwargs):
        return {**data, "student_count": len(data["students"])}


classroomSchema = ClassroomSchema()