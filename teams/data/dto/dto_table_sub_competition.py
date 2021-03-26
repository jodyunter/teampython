from teams.data.dto.dto_sub_competition import SubCompetitionDTO
from teams.domain.sub_competition import TableSubCompetition


# todo: create repo
class TableSubCompetitionDTO(SubCompetitionDTO, TableSubCompetition):
    __mapper_args__ = {
        'polymorphic_identity': 'table_sub_competition'
    }

    def __init__(self, table_sub_competition):
        TableSubCompetition.__init__(self,
                                     table_sub_competition.name,
                                     table_sub_competition.records,
                                     table_sub_competition.competition,
                                     table_sub_competition.groups,
                                     table_sub_competition.order,
                                     table_sub_competition.setup,
                                     table_sub_competition.started,
                                     table_sub_competition.finished,
                                     table_sub_competition.post_processed,
                                     table_sub_competition.oid)
