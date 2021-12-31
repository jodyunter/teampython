from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship

# these imports are required to let python know we need these defined BEFORE this class
from teams.data.dto.dto_competition_team import CompetitionTeamDTO
from teams.data.dto.dto_sub_competition import SubCompetitionDTO
from teams.data.dto.dto_table_sub_competition import TableSubCompetitionDTO
from teams.data.dto.dto_record import RecordDTO
from teams.domain.competition import TableRecord


class TableRecordDTO(RecordDTO, TableRecord):
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("TableSubCompetitionDTO", foreign_keys=[sub_competition_id])

    __mapper_args__ = {
        'polymorphic_identity': 'table_record'
    }

    def __init__(self, table_record):
        sub_competition = TableSubCompetitionDTO.get_dto(table_record.sub_competition)
        team = CompetitionTeamDTO.get_dto(table_record.team)

        TableRecord.__init__(self,
                             sub_competition,
                             table_record.rank,
                             team,
                             table_record.year,
                             table_record.wins,
                             table_record.loses,
                             table_record.ties,
                             table_record.goals_for,
                             table_record.goals_against,
                             table_record.skill,
                             table_record.oid)

        @staticmethod
        def get_dto(record):
            if record.__class__ == TableRecordDTO:
                return record
            else:
                return TableRecordDTO(record)