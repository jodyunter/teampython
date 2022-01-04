from teams.data.repo.repository import Repository
from teams.domain.series import Series
from teams.domain.series_by_goals import SeriesByGoals
from teams.domain.series_by_wins import SeriesByWins


class SeriesRepository(Repository):

    def get_type(self):
        return Series


class SeriesByGoalsRepository(SeriesRepository):

    def get_type(self):
        return SeriesByGoals


class SeriesByWinsRepository(SeriesRepository):

    def get_type(self):
        return SeriesByWins
