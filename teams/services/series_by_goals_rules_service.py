from teams.data.repo.rules_repository import GameRulesRepository, \
    SeriesByGoalsRulesRepository
from teams.domain.series_by_goals_rules import SeriesByGoalsRules
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.services.base_service import BaseService
from teams.services.view_models import get_model


class SeriesByGoalsRulesService(BaseService):

    def get_repo(self):
        return self.repo

    repo = SeriesByGoalsRulesRepository()
    game_rules_repo = GameRulesRepository()

    def create(self, series_name, games_to_play, game_rules_id, last_game_rules_id, home_progression, session=None):
        commit = session is None
        session = self.get_session(session)

        game_rules = self.game_rules_repo.get_by_oid(game_rules_id, session)
        last_game_rules = self.game_rules_repo.get_by_oid(last_game_rules_id, session)

        series_rules = SeriesByGoalsRules(series_name, games_to_play, game_rules, last_game_rules, home_progression)

        self.repo.add(series_rules, session, SeriesByWinsRules)

        self.commit(session, commit)

        return get_model.get_vm(series_rules)


