from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teams.domain.base import Base
from teams.domain.competition import Competition
from teams.domain.competition_game import CompetitionGame
from teams.domain.competition_group import CompetitionGroup
from teams.domain.competition_ranking import CompetitionRanking
from teams.domain.game import Game
from teams.domain.game_rules import GameRules
from teams.domain.gamedata import GameData
from teams.domain.record import Record
from teams.domain.series import Series
from teams.domain.series_game import SeriesGame
from teams.domain.series_rules import SeriesRules
from teams.domain.sub_competition import SubCompetition
from teams.domain.team import Team

engine = None
Session = sessionmaker()


class Database:
    @staticmethod
    def get_engine():
        global engine
        return engine

    @staticmethod
    def create_db(file):
        global engine
        engine = create_engine(file)

    @staticmethod
    def init_db(file):
        global engine
        engine = create_engine(file)
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def clean_up_database(session):
        session.query(SeriesGame).delete()
        session.query(CompetitionRanking).delete()
        session.query(CompetitionGroup).delete()
        session.query(SeriesRules).delete()
        session.query(Series).delete()
        session.query(Competition).delete()
        session.query(SubCompetition).delete()
        session.query(CompetitionGame).delete()
        session.query(Game).delete()
        session.query(Record).delete()
        session.query(Team).delete()
        session.query(GameRules).delete()
        session.query(GameData).delete()
        session.commit()
        session.flush()

    @staticmethod
    def get_session():
        return Session()
