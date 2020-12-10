from teams.data.database import Creation, Database, ClearData


class TestBaseRepository:
    @staticmethod
    def setup_database():
        Creation.create_db("sqlite:///:memory:")

    @staticmethod
    def setup_basic_test():
        TestBaseRepository.setup_database()
        session = Database.get_session()
        ClearData.clean_up_database(session)
        return session