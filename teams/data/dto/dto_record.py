from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_team import TeamDTO
from teams.domain.record import Record


class RecordDTO(Base, Record):
    __tablename__ = "records"

    oid = Column(String, primary_key=True)
    rank = Column(Integer)
    year = Column(Integer)
    wins = Column(Integer, default=0)
    loses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    skill = Column(Integer, default=0)
    team_id = Column(String, ForeignKey('teams.oid'))
    team = relationship("TeamDTO")
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'record'
    }

    def __init__(self, record):
        team_dto = TeamDTO.get_dto(record.team)
        Record.__init__(self, record.rank, team_dto, record.year, record.wins, record.loses, record.ties, record.goals_for,
                        record.goals_against, record.skill, record.oid)

    @staticmethod
    def get_dto(record):
        if record.__class__ == RecordDTO:
            return record
        else:
            return RecordDTO(record)

    def __eq__(self, o):
        return self.rank == o.rank and \
               self.team == o.team and \
               self.year == o.year and \
               self.wins == o.wins and \
               self.loses == o.loses and \
               self.ties == o.ties and \
               self.goals_for == o.goals_for and \
               self.goals_against == o.goals_against and \
               self.skill == o.skill and \
               self.oid == o.oid





