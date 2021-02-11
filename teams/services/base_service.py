import uuid

from teams.data.database import Database
from teams.domain.utility.utility_classes import IDHelper


class BaseService:
    @staticmethod
    def get_new_id():
        return IDHelper.get_new_id()

    @staticmethod
    def get_session(session=None):
        if session is None:
            session = Database.get_session()

        return session

    @staticmethod
    def commit(session, commit):
        if commit:
            session.commit()
