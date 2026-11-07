from marshmallow import Schema, fields, EXCLUDE, validates, ValidationError, post_load
import re
import operator


class UserSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    age = fields.Integer(required=True)


userSchema = UserSchema()


class UserFilterSchema(Schema):
    filter_by = fields.String(load_default=None)

    class Meta():
        unknown = EXCLUDE

    # two-char operators must come before one-char ones, or "age<=30" matches "<" with value "=30"
    FILTER_PATTERN = re.compile(r"^(\w+)(<=|>=|!=|=|<|>)(.+)$")
    OPERATORS = {
        "<=": operator.le,
        ">=": operator.ge,
        "!=": operator.ne,
        "=": operator.eq,
        "<": operator.lt,
        ">": operator.gt
    }
    FILTERABLE_FIELDS = {"age": int}

    @validates("filter_by")
    def validate_filter_by(self, value, **kwargs):
        if value is None:
            return
        match = self.FILTER_PATTERN.match(value)
        if match is None:
            raise ValidationError(
                f"Must be <field><op><value>, op one of: {','.join(self.OPERATORS)}")
        field, op, raw = match.groups()
        if field not in self.FILTERABLE_FIELDS:
            raise ValidationError(
                f"Cannot filter by '{field}'. Allowed: {list(self.FILTERABLE_FIELDS)}")
        try:
            self.FILTERABLE_FIELDS[field](raw)
        except ValueError:
            raise ValidationError(f"Invalid value for '{field}': {raw}")

    @post_load
    def parse_filter_by(self, data, **kwargs):
        if data.get("filter_by"):
            field, op, value_raw = self.FILTER_PATTERN.match(
                data["filter_by"]).groups()
            cast = self.FILTERABLE_FIELDS[field]
            data["filter_by"] = (field, self.OPERATORS[op], cast(value_raw))
        return data


userFilterSchema = UserFilterSchema()


class UserSortSchema(Schema):
    sort_by = fields.String(load_default=None)

    class Meta():
        unknown = EXCLUDE

    # field.asc/desc
    SORT_PATTERN = re.compile(r"(\w+)\.(\w+)")
    SORTABLE_FIELDS = ["age"]
    SORTABLE_DIRECTION = ["asc", "desc"]

    @validates("sort_by")
    def validate_sort_by(self, value, **kwargs):
        if value is None:
            return

        # check that the value matches the field.asc/desc pattern
        match = self.SORT_PATTERN.fullmatch(value)
        if match is None:
            raise ValidationError(
                f"Must be <field>.<sort direction>, direction one of: {','.join(self.SORTABLE_DIRECTION)}")
        field, sort_direction = match.groups()

        # check that the field is sortable
        if field not in self.SORTABLE_FIELDS:
            raise ValidationError(
                f"Cannot sort by '{field}'. Allowed: {list(self.SORTABLE_FIELDS)}")

        # check that the direction is asc/desc
        if sort_direction not in self.SORTABLE_DIRECTION:
            raise ValidationError(
                f"Invalid sort direction '{sort_direction}'. Allowed: {list(self.SORTABLE_DIRECTION)}")

    @post_load
    def parse_sort_by(self, data, **kwargs):
        if data.get("sort_by"):
            field, descending_str = self.SORT_PATTERN.fullmatch(
                data["sort_by"]).groups()
            descending = True if descending_str == "desc" else False
            data["sort_by"] = (field, descending)
        return data


userSortSchema = UserSortSchema()
