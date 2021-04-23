import pytest

from teams.data.database import Database
from teams.domain.utility.utility_classes import IDHelper


class TestBaseRepository:
    @staticmethod
    def setup_database():
        Database.init_db("sqlite:///:memory:")

    @staticmethod
    def setup_basic_test():
        TestBaseRepository.setup_database()
        session = Database.get_session()
        Database.clean_up_database(session)
        return session

    @staticmethod
    def get_id():
        return IDHelper.get_new_id()
