from teams.data.dto.dto_sub_competition import SubCompetitionDTO
from teams.domain.sub_competition import PlayoffSubCompetition


class PlayoffSubCompetitionDTO(SubCompetitionDTO, PlayoffSubCompetition):
    __mapper_args__ = {
        'polymorphic_identity': 'playoff_sub_competition'
    }

    def __init__(self, playoff_sub_competition):
        PlayoffSubCompetition.__init__(self,
                                       playoff_sub_competition.name,
                                       playoff_sub_competition.series,
                                       playoff_sub_competition.competition,
                                       playoff_sub_competition.groups,
                                       playoff_sub_competition.order,
                                       playoff_sub_competition.current_round,
                                       playoff_sub_competition.setup,
                                       playoff_sub_competition.started,
                                       playoff_sub_competition.finished,
                                       playoff_sub_competition.post_processed,
                                       playoff_sub_competition.oid)
