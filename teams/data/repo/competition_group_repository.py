from teams.data.repo.repository import Repository
from teams.domain.sub_competition import CompetitionGroup, RankingGroup


class CompetitionGroupRepository(Repository):

    def get_type(self):
        return CompetitionGroup


class RankingGroupRepository(Repository):

    def get_type(self):
        return RankingGroup

