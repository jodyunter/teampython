from unittest import TestCase

from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.domain.game import GameRules
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestGameRulesRepository(TestBaseRepository, TestCase):
    repo = GameRulesRepository()

    def test_add(self):
        session = self.setup_basic_test()
        self.repo.add(GameRules("My Name", False, self.get_id()), session)
        session.commit()

        self.assertEqual(1, len(self.repo.get_all(session)))