from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.record import Record


class RecordDTO(Base, Record):
    __tablename__ = "records"

    oid = Column(String, primary_key=True)
    year = Column(Integer)
    wins = Column(Integer, default=0)
    loses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    team_id = Column(Integer, ForeignKey('teams.oid'))
    team = relationship("TeamDTO")

    def __init__(self, team, year, wins, loses, ties, goals_for, goals_against, oid):
        self.oid = oid
        self.year = year
        self.team = team
        self.wins = wins
        self.loses = loses
        self.ties = ties
        self.goals_for = goals_for
        self.goals_against = goals_against
