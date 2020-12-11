import uuid


class BaseService:
    @staticmethod
    def get_new_id():
        return str(uuid.uuid4())
