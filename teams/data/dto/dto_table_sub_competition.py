from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_competition_group import CompetitionGroupDTO
from teams.data.dto.dto_sub_competition import SubCompetitionDTO
from teams.data.dto.dto_table_record import TableRecordDTO
from teams.domain.sub_competition import TableSubCompetition


class TableSubCompetitionDTO(SubCompetitionDTO, TableSubCompetition):
    __mapper_args__ = {
        'polymorphic_identity': 'table_sub_competition'
    }

    def __init__(self, table_sub_competition):
        competition = CompetitionDTO.get_dto(table_sub_competition.compettiion)
        groups = [CompetitionGroupDTO.get_dto(g) for g in table_sub_competition.groups]
        records = [
            TableRecordDTO(r) for r in table_sub_competition.records]
        TableSubCompetition.__init__(self,
                                     table_sub_competition.name,
                                     records,
                                     competition,
                                     groups,
                                     table_sub_competition.order,
                                     table_sub_competition.setup,
                                     table_sub_competition.started,
                                     table_sub_competition.finished,
                                     table_sub_competition.post_processed,
                                     table_sub_competition.oid)

    @staticmethod
    def get_dto(table_sub_competition):
        if table_sub_competition.__class__ == TableSubCompetitionDTO:
            return table_sub_competition
        else:
            return TableSubCompetitionDTO(table_sub_competition)