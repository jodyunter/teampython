# mapped
from sqlalchemy import Column, String, Integer, Boolean

from teams.data.dto.dto_base import Base


class GameData(Base):
    __tablename__ = "gamedata"

    name = Column(String, primary_key=True)
    current_day = Column(Integer)
    current_year = Column(Integer)
    is_year_setup = Column(Boolean)
    is_year_finished = Column(Boolean)

    def __init__(self, name, current_year, current_day, is_year_setup, is_year_finished):
        self.name = name
        self.current_year = current_year
        self.current_day = current_day
        self.is_year_setup = is_year_setup
        self.is_year_finished = is_year_finished
        self.oid = None

    def __eq__(self, other):
        return self.name == other.name and \
            self.current_day == other.current_day and \
            self.current_year == other.current_year and \
            self.is_year_setup == other.is_year_setup and \
            self.is_year_finished == other.is_year_finished