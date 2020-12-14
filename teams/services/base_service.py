import uuid

from teams.data.database import Database


class BaseService:
    @staticmethod
    def get_session():
        return Database.get_session()

    @staticmethod
    def get_new_id():
        return str(uuid.uuid4())

    @staticmethod
    def should_commit(session):
        if session is None:
            session = BaseService.get_session()
            return False
        else:
            return True

    @staticmethod
    def commit(should_commit, session):
        if should_commit:
            session.commit()
