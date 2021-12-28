from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_series_by_goals_rules import SeriesByGoalsRulesDTO
from teams.data.dto.dto_series_by_wins_rules import SeriesByWinsRulesDTO
from teams.data.dto.dto_series_rules import SeriesRulesDTO
from teams.data.repo.repository import Repository


class GameRulesRepository(Repository):

    def get_type(self):
        return GameRulesDTO

    def get_by_name(self, name, session):
        return session.query(GameRulesDTO).filter_by(name=name).first()


class SeriesRulesRepository(Repository):

    def get_type(self):
        return SeriesRulesDTO


class SeriesByWinsRulesRepository(Repository):

    def get_type(self):
        return SeriesByWinsRulesDTO


class SeriesByGoalsRulesRepository(Repository):

    def get_type(self):
        return SeriesByGoalsRulesDTO