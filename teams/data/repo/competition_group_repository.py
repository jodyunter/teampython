from teams.data.dto.dto_competition_group import CompetitionGroupDTO
from teams.data.dto.dto_ranking_group import RankingGroupDTO
from teams.data.repo.repository import Repository


class CompetitionGroupRepository(Repository):

    def get_type(self):
        return CompetitionGroupDTO


class RankingGroupRepository(Repository):

    def get_type(self):
        return RankingGroupDTO

