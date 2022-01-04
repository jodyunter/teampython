from unittest import TestCase

from teams.services.game_rules_service import GameRulesService
from teams.services.series_rules_service import SeriesRulesService
from teams.services.view_models.playoff_view_models import SeriesByGoalsRulesViewModel, SeriesByWinsRulesViewModel
from tests.teams.services.base_test_service import BaseTestService


class TestSeriesRulesService(BaseTestService, TestCase):
    service = SeriesRulesService()
    game_rules_service = GameRulesService()

    def test_create(self):
        pass

    def setup_list(self, session=None):
        commit = session is None
        session = self.service.get_session()
        game_rules1 = self.game_rules_service.create("Game Rules", True, session)
        game_rules2 = self.game_rules_service.create("Game Rules 2", True, session)
        game_rules3 = self.game_rules_service.create("Game Rules 3", True, session)
        results = [
            self.service.create_series_by_goals_rules("Goals Test Rules A", 4, game_rules1.oid, game_rules2.oid, [1],
                                                      session),
            self.service.create_series_by_goals_rules("Goals Test Rules B", 3, game_rules2.oid, game_rules3.oid, [1, 1],
                                                      session),
            self.service.create_series_by_goals_rules("Goals Test Rules C", 2, game_rules3.oid, game_rules1.oid,
                                                      [1, 1, 0], session),
            self.service.create_series_by_goals_rules("Goals Test Rules D", 1, game_rules1.oid, game_rules2.oid,
                                                      [1, 1, 0, 0], session),
            self.service.create_series_by_goals_rules("Goals Test Rules E", 6, game_rules2.oid, game_rules3.oid,
                                                      [1, 1, 0, 0, 0], session),
            self.service.create_series_by_wins_rules("Wins Test Rules A", 4, game_rules1.oid, [1], session),
            self.service.create_series_by_wins_rules("Wins Test Rules B", 3, game_rules2.oid, [1, 1], session),
            self.service.create_series_by_wins_rules("Wins Test Rules C", 2, game_rules3.oid, [1, 1, 0], session),
            self.service.create_series_by_wins_rules("Wins Test Rules D", 1, game_rules1.oid, [1, 1, 0, 0], session),
            self.service.create_series_by_wins_rules("Wins Test Rules E", 6, game_rules2.oid, [1, 1, 0, 0, 0], session)]
        self.service.commit(session, commit)

        return results

    def test_create_by_wins(self):
        self.setup_test()
        game_rules = self.game_rules_service.create("These game rules", False)
        rules_vm = self.service.create_series_by_wins_rules("Test Rules Create", 4, game_rules.oid, [1])

        self.assertIsNotNone(rules_vm.oid)
        self.assertEqual(game_rules.oid, rules_vm.game_rules.oid)

        self.assertEqual("Test Rules Create", rules_vm.name)
        self.assertTrue(4, rules_vm.required_wins)
        self.assertEqual([1], rules_vm.home_pattern)

    def test_create_by_goals(self):
        self.setup_test()
        game_rules = self.game_rules_service.create("These game rules", False)
        game_rules2 = self.game_rules_service.create("These game rules2", False)
        rules_vm = self.service.create_series_by_goals_rules("Test Rules Create", 4, game_rules.oid, game_rules2.oid, [1])

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

        self.assertEqual(10, len(all_rules))
        all_names = [rule.name for rule in all_rules]
        self.assertTrue("Goals Test Rules A" in all_names)
        self.assertTrue("Goals Test Rules B" in all_names)
        self.assertTrue("Goals Test Rules C" in all_names)
        self.assertTrue("Goals Test Rules D" in all_names)
        self.assertTrue("Goals Test Rules E" in all_names)
        self.assertTrue("Wins Test Rules A" in all_names)
        self.assertTrue("Wins Test Rules B" in all_names)
        self.assertTrue("Wins Test Rules C" in all_names)
        self.assertTrue("Wins Test Rules D" in all_names)
        self.assertTrue("Wins Test Rules E" in all_names)

    def test_get_by_id(self):
        self.setup_test()
        data = self.setup_list()

        goals = data[3]
        wins = data[8]

        goal_result = self.service.get_by_id(goals.oid)
        self.assertEqual(goal_result.oid, goals.oid)
        self.assertTrue(isinstance(goal_result, SeriesByGoalsRulesViewModel))

        win_result = self.service.get_by_id(wins.oid)
        self.assertEqual(win_result.oid, wins.oid)
        self.assertTrue(isinstance(win_result, SeriesByWinsRulesViewModel))