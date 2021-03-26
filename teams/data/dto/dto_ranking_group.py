from teams.data.dto.dto_competition_group import CompetitionGroupDTO
from teams.domain.competition import RankingGroup

# todo: create repo
class RankingGroupDTO(CompetitionGroupDTO, RankingGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'ranking_group'
    }

    def __init__(self, competition_group):
        RankingGroup.__init__(self,
                              competition_group.name,
                              competition_group.parent_group,
                              competition_group.sub_competition,
                              competition_group.level,
                              competition_group.rankings,
                              competition_group.oid)