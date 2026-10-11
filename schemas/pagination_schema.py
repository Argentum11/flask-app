from marshmallow import Schema, fields


class PaginationSchema(Schema):
    limit = fields.Integer(load_default=None)
    offset = fields.Integer(load_default=0)


paginationSchema = PaginationSchema()
