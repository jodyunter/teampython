from teams.data.repo.rules_repository import SeriesByWinsRulesRepository, GameRulesRepository
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.services.base_service import BaseService
from teams.services.view_models import get_model


class SeriesByWinsRulesService(BaseService):

    def get_repo(self):
        return self.repo

    repo = SeriesByWinsRulesRepository()
    game_rules_repo = GameRulesRepository()

    def create(self, series_name, required_wins, rules_id, home_progression, session=None):
        commit = session is None
        session = self.get_session(session)

        rules = self.game_rules_repo.get_by_oid(rules_id, session)

        series_rules = SeriesByWinsRules(series_name, required_wins, rules, home_progression)

        self.repo.add(series_rules, session, SeriesByWinsRules)

        self.commit(session, commit)

        return get_model.get_vm(series_rules)


