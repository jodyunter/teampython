import uuid

from teams.data.database import Database


class BaseService:
    @staticmethod
    def get_session():
        return Database.get_session()

    @staticmethod
    def get_new_id():
        return str(uuid.uuid4())
