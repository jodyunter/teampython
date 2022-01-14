from teams.data.repo.repository import Repository
from teams.domain import CompetitionConfiguration, TableSubCompetitionConfiguration, CompetitionTeamConfiguration
from teams.domain.competition_group_configuration import RankingGroupConfiguration


class CompetitionConfigurationRepository(Repository):
    def get_type(self):
        return CompetitionConfiguration


class TableSubCompetitionConfigurationRepository(Repository):
    def get_type(self):
        return TableSubCompetitionConfiguration


class RankingGroupConfigurationRepository(Repository):
    def get_type(self):
        return RankingGroupConfiguration


class CompetitionTeamConfigurationRepository(Repository):
    def get_type(self):
        return CompetitionTeamConfiguration