from teams.data.database import Database
from teams.data.dto.dto_series_by_wins_rules import SeriesByWinsRulesDTO
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.data.repo.repository import BasicRepository
from teams.domain.series_rules import SeriesByWinsRules
from teams.services.base_service import BaseService
from teams.services.game_service import GameRulesService


class ConfigurationService(BaseService):

    def create_best_of_series_rules(self, series_name, required_wins, rules_id, home_progression, session=None):
        commit = session is None
        session = self.get_session(session)

        repo = BasicRepository()
        game_rules_repo = GameRulesRepository()
        rules = game_rules_repo.get_by_oid(rules_id)

        series_rules = SeriesByWinsRules(series_name, required_wins, rules, home_progression)

        repo.add(series_rules, session, SeriesByWinsRulesDTO)

        self.commit(session, commit)
