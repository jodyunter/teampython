from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_record import RecordDTO
from teams.data.dto.dto_team import TeamDTO

engine = None
Session = sessionmaker()


class Creation:
    @staticmethod
    def create_db(file):
        global engine
        engine = create_engine(file)
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)


class ClearData:
    @staticmethod
    def clean_up_database(session):
        session.query(TeamDTO).delete()
        session.query(RecordDTO).delete()
        session.commit()
        session.flush()


class Database:
    @staticmethod
    def get_session():
        return Session()
