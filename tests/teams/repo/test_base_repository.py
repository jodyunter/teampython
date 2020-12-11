import uuid

from teams.data.database import Database


class TestBaseRepository:
    @staticmethod
    def setup_database():
        Database.create_db("sqlite:///:memory:")

    @staticmethod
    def setup_basic_test():
        TestBaseRepository.setup_database()
        session = Database.get_session()
        Database.clean_up_database(session)
        return session

    @staticmethod
    def get_id():
        return str(uuid.uuid4())