from teams.data.repo.rules_repository import SeriesRulesRepository
from teams.services.base_service import BaseService
from teams.services.series_by_goals_rules_service import SeriesByGoalsRulesService
from teams.services.series_by_wins_rules_service import SeriesByWinsRulesService


class SeriesRulesService(BaseService):
    by_goals_service = SeriesByGoalsRulesService()
    by_wins_service = SeriesByWinsRulesService()

    def get_repo(self):
        return SeriesRulesRepository()

    def create_series_by_goals_rules(self, series_name, games_to_play, game_rules_id, last_game_rules_id, home_progression, session=None):
        return self.by_goals_service.create(series_name, games_to_play, game_rules_id, last_game_rules_id, home_progression, session)

    def create_series_by_wins_rules(self, series_name, required_wins, rules_id, home_progression, session=None):
        return self.by_wins_service.create(series_name, required_wins, rules_id, home_progression, session)