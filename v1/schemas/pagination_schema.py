from marshmallow import Schema, fields, EXCLUDE


class PaginationSchema(Schema):
    limit = fields.Integer(load_default=None)
    offset = fields.Integer(load_default=0)

    class Meta():
        unknown = EXCLUDE

paginationSchema = PaginationSchema()
