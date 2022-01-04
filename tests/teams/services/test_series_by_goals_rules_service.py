from unittest import TestCase

from teams.services.game_rules_service import GameRulesService
from teams.services.series_by_goals_rules_service import SeriesByGoalsRulesService
from teams.services.series_by_wins_rules_service import SeriesByWinsRulesService
from tests.teams.services.test_team_service import BaseTestService


class TestSeriesByGoalsRulesService(BaseTestService, TestCase):
    service = SeriesByGoalsRulesService()
    game_rules_service = GameRulesService()

    def setup_list(self, session=None):
        commit = session is None
        session = self.service.get_session()
        game_rules1 = self.game_rules_service.create("Game Rules", True, session)
        game_rules2 = self.game_rules_service.create("Game Rules 2", True, session)
        game_rules3 = self.game_rules_service.create("Game Rules 3", True, session)

        self.service.create("Test Rules A", 4, game_rules1.oid, game_rules2.oid, [1], session)
        self.service.create("Test Rules B", 3, game_rules2.oid, game_rules3.oid, [1, 1], session)
        self.service.create("Test Rules C", 2, game_rules3.oid, game_rules1.oid, [1, 1, 0], session)
        self.service.create("Test Rules D", 1, game_rules1.oid, game_rules2.oid, [1, 1, 0, 0], session)
        self.service.create("Test Rules E", 6, game_rules2.oid, game_rules3.oid, [1, 1, 0, 0, 0], session)
        self.service.commit(session, commit)

    def test_create(self):
        self.setup_test()
        game_rules = self.game_rules_service.create("These game rules", False)
        game_rules2 = self.game_rules_service.create("These game rules2", False)
        rules_vm = self.service.create("Test Rules Create", 4, game_rules.oid, game_rules2.oid, [1])

        self.assertIsNotNone(rules_vm.oid)
        self.assertEqual(game_rules.oid, rules_vm.game_rules.oid)
        self.assertEqual(game_rules2.oid, rules_vm.last_game_rules.oid)

        self.assertEqual("Test Rules Create", rules_vm.name)
        self.assertTrue(4, rules_vm.games_to_play)
        self.assertEqual([1], rules_vm.home_pattern)

    def test_get_all(self):
        self.setup_test()
        self.setup_list()

        all_rules = self.service.get_all()

        self.assertEqual(5, len(all_rules))
        all_names = [rule.name for rule in all_rules]
        self.assertTrue("Test Rules A" in all_names)
        self.assertTrue("Test Rules B" in all_names)
        self.assertTrue("Test Rules C" in all_names)
        self.assertTrue("Test Rules D" in all_names)
        self.assertTrue("Test Rules E" in all_names)
