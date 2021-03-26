from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship

from teams.data.dto.dto_record import RecordDTO
from teams.domain.competition import TableRecord


# todo: create repo
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