from flask_restful import Resource
from marshmallow import Schema, fields, pre_dump
from controllers.user_controller import userModel, UserSchema


class ClassroomSchema(Schema):
    class_id = fields.Integer(dump_only=True)
    class_name = fields.String(required=True)
    students = fields.List(fields.Nested(UserSchema), required=True)
    student_count = fields.Integer(dump_only=True)

    @pre_dump
    def add_student_count(self, data, **kwargs):
        return {**data, "student_count": len(data["students"])}


classroomSchema = ClassroomSchema()


class ClassroomResource(Resource):
    def __init__(self):
        self.classrooms = {
            0: {
                "class_id": 0,
                "class_name": "class_a",
                "students": [0, 1]
            },
            1: {
                "class_id": 1,
                "class_name": "class_b",
                "students": [2]
            }
        }

    def get(self, classroom_id=None):
        if classroom_id is None:
            updated_classroom = [self.update_classroom_students(
                classroom) for classroom in self.classrooms.values()]
            return classroomSchema.dump(updated_classroom, many=True)
        classroom = self.classrooms.get(classroom_id, None)
        if classroom is None:
            return {"error": "classroom not found!"}, 404
        return classroomSchema.dump(self.update_classroom_students(classroom))

    def update_classroom_students(self, classroom):
        classroom_copy = classroom.copy()
        classroom_copy["students"] = [userModel.get_users(
            user_id) for user_id in classroom_copy["students"]]
        return classroom_copy
