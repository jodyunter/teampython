import uuid

from teams.data.database import Database


class BaseService:
    @staticmethod
    def get_new_id():
        return str(uuid.uuid4())

    @staticmethod
    def get_session(session=None):
        if session is None:
            session = Database.get_session()

        return session

    @staticmethod
    def commit(session, commit):
        if commit:
            session.commit()
