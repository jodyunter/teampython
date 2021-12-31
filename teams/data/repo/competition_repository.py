from teams.data.repo.repository import Repository
from teams.domain.competition import Competition
from teams.domain.sub_competition import SubCompetition, TableSubCompetition, PlayoffSubCompetition


class CompetitionRepository(Repository):

    def get_type(self):
        return Competition


class SubCompetitionRepository(Repository):

    def get_type(self):
        return SubCompetition


class TableSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return TableSubCompetition


class PlayoffSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return PlayoffSubCompetition
