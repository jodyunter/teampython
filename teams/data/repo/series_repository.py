from teams.data.dto.dto_series import SeriesDTO
from teams.data.dto.dto_series_by_goals import SeriesByGoalsDTO
from teams.data.dto.dto_series_by_wins import SeriesByWinsDTO
from teams.data.repo.repository import Repository


class SeriesRepository(Repository):

    def get_type(self):
        return SeriesDTO


class SeriesByGoalsRepository(Repository):

    def get_type(self):
        return SeriesByGoalsDTO


class SeriesByWinsRepository(Repository):

    def get_type(self):
        return SeriesByWinsDTO
