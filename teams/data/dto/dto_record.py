from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_team import TeamDTO
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

    def __init__(self, record):
        team_dto = TeamDTO.get_dto(record.team)
        Record.__init__(self, team_dto, record.year, record.wins, record.loses, record.ties, record.goals_for,
                        record.goals_against, record.oid)

    @staticmethod
    def get_dto(record):
        if record.__class__ == RecordDTO:
            return record
        else:
            return RecordDTO(record)
