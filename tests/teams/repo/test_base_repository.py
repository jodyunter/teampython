import uuid

import pytest

from teams.data.database import Database
from teams.data.repo.base_repository import BaseRepository


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
        return str(uuid.uuid4())

    def test_basic_get_type(self):
        base_repo = BaseRepository()
        with pytest.raises(NotImplementedError):
            base_repo.get_type()
