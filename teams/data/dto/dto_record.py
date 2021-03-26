from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_team import TeamDTO
from teams.data.dto.dto_sub_competition import TableSubCompetitionDTO
from teams.domain.competition import TableRecord
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


class TableRecordDTO(RecordDTO, TableRecord):
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("TableSubCompetitionDTO", foreign_keys=[sub_competition_id])

    __mapper_args__ = {
        'polymorphic_identity': 'table_record'
    }

    def __init__(self, table_record):
        TableRecord.__init__(self,
                             table_record.sub_competition,
                             table_record.rank,
                             table_record.team,
                             table_record.year,
                             table_record.wins,
                             table_record.loses,
                             table_record.ties,
                             table_record.goals_for,
                             table_record.goals_against,
                             table_record.skill,
                             table_record.oid)