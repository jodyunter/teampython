from sqlalchemy import Column, Integer, String, Boolean

from teams.data.dto.dto_base import Base
from teams.domain.gamedata import GameData


class GameDataDTO(Base, GameData):
    __tablename__ = "gamedata"

    name = Column(String, primary_key=True)
    current_day = Column(Integer)
    current_year = Column(Integer)
    is_year_setup = Column(Boolean)
    is_year_finished = Column(Boolean)

    def __init__(self, game_data):
        self.oid = None
        GameData.__init__(self, game_data.name, game_data.current_day, game_data.current_year,
                          game_data.is_year_setup, game_data.is_year_finished)

    def __eq__(self, other):
        return self.name == other.name and \
            self.current_day == other.current_day and \
            self.current_year == other.current_year and \
            self.is_year_setup == other.is_year_setup and \
            self.is_year_finished == other.is_year_finished

