from unittest import TestCase

from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.domain.game import GameRules
from tests.teams.repo.test_repository import BaseRepoTests


class GameRulesRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return GameRulesRepository()

    def get_add_record(self):
        return GameRulesDTO(GameRules("Rules Name", False))

    def get_updated_record(self, original_record):
        original_record.name = "New Name"
        original_record.can_tie = True
        return original_record

    def test_add(self):
        session = self.setup_basic_test()
        self.get_repo().add(GameRules("My Name", False, self.get_id()), session)
        session.commit()

        self.assertEqual(1, len(self.get_repo().get_all(session)))
