from sqlalchemy import types


class IntArrayString(types.TypeDecorator):
    @property
    def python_type(self):
        return [].__class__

    def process_literal_param(self, value, dialect):
        pass

    impl = types.String

    def process_bind_param(self, value, dialect):
        if value is None or len(value) == 0:
            return ""

        return ",".join([str(k) for k in value])

    def process_result_value(self, value, dialect):
        result = []
        if len(value) > 0:
            for i in value.split(","):
                result.append(int(i))

        return result

