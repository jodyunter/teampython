from teams.data.repo.repository import BasicRepository
from teams.data.repo.rules_repository import GameRulesRepository
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.services.base_service import BaseService


class ConfigurationService(BaseService):

    def create_best_of_series_rules(self, series_name, required_wins, rules_id, home_progression, session=None):
        commit = session is None
        session = self.get_session(session)

        repo = BasicRepository()
        game_rules_repo = GameRulesRepository()
        rules = game_rules_repo.get_by_oid(rules_id)

        series_rules = SeriesByWinsRules(series_name, required_wins, rules, home_progression)

        repo.add(series_rules, session, SeriesByWinsRules)

        self.commit(session, commit)

        return series_rules
