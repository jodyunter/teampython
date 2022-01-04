from teams.data.repo.rules_repository import GameRulesRepository
from teams.domain.game_rules import GameRules
from teams.services.base_service import BaseService
from teams.services.view_models import GetModel


class GameRulesService(BaseService):
    repo = GameRulesRepository()

    def get_repo(self):
        return self.repo

    def create(self, name, can_tie, session=None):
        commit = session is None
        session = self.get_session(session)

        rules = GameRules(name, can_tie, self.get_new_id())
        self.get_repo().add(rules, session)

        self.commit(session, commit)

        return GetModel.get_vm(rules)

    def get_by_name(self, name, session=None):
        session = self.get_session(session)

        rules = self.get_repo().get_by_name(name, session)

        return GetModel.get_vm(rules)
