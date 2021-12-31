from teams.data.repo.repository import Repository
from teams.domain.game import GameRules
from teams.domain.series_by_goals_rules import SeriesByGoalsRules
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.domain.series_rules import SeriesRules


class GameRulesRepository(Repository):

    def get_type(self):
        return GameRules

    def get_by_name(self, name, session):
        return session.query(self.get_type()).filter_by(name=name).first()


class SeriesRulesRepository(Repository):

    def get_type(self):
        return SeriesRules


class SeriesByWinsRulesRepository(Repository):

    def get_type(self):
        return SeriesByWinsRules


class SeriesByGoalsRulesRepository(Repository):

    def get_type(self):
        return SeriesByGoalsRules
