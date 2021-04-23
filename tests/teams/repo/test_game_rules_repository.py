from unittest import TestCase

from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.domain.game import GameRules
from tests.teams.repo.test_repository import TestBaseRepository


class TestGameRulesRepository(TestBaseRepository, TestCase):

    def test_add(self):
        session = self.setup_basic_test()
        GameRulesRepository.add(GameRules("My Name", False, self.get_id()), GameRulesDTO, session)
        session.commit()

        self.assertEqual(1, len(GameRulesRepository.get_all(GameRulesDTO, session)))
