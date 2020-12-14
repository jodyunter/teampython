from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_configuration import ConfigurationItemDTO
from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_record import RecordDTO
from teams.data.dto.dto_team import TeamDTO

engine = None
Session = sessionmaker()


class Database:
    @staticmethod
    def create_db(file):
        global engine
        engine = create_engine(file)
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def clean_up_database(session):
        session.query(GameDTO).delete()
        session.query(RecordDTO).delete()
        session.query(TeamDTO).delete()
        session.query(GameRulesDTO).delete()
        session.query(ConfigurationItemDTO).delete()
        session.commit()
        session.flush()

    @staticmethod
    def get_session():
        return Session()
