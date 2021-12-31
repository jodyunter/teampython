from teams.data.repo.repository import Repository
from teams.domain.series import Series, SeriesByGoals, SeriesByWins


class SeriesRepository(Repository):

    def get_type(self):
        return Series


class SeriesByGoalsRepository(Repository):

    def get_type(self):
        return SeriesByGoals


class SeriesByWinsRepository(Repository):

    def get_type(self):
        return SeriesByWins
