from unittest import TestCase

from teams.data.repo.rules_repository import GameRulesRepository, SeriesRulesRepository
from teams.domain.game_rules import GameRules
from teams.domain.series_rules import SeriesRules
from tests.teams.repo.test_repository import BaseRepoTests


class GameRulesRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return GameRulesRepository()

    def get_add_record(self):
        return GameRules("Rules Name", False)

    def get_updated_record(self, original_record):
        original_record.name = "New Name"
        original_record.can_tie = True
        return original_record

    def test_add(self):
        session = self.setup_basic_test()
        self.get_repo().add(GameRules("My Name", False, self.get_id()), session)
        session.commit()

        self.assertEqual(1, len(self.get_repo().get_all(session)))


class TestSeriesRulesRepository(BaseRepoTests, TestCase):
    def get_repo(self):
        return SeriesRulesRepository()

    def get_game_rules_repo(self):
        return GameRulesRepository()

    def get_add_record(self):
        return SeriesRules("Test Rule", GameRules("My Rules", False), SeriesRules.WINS_TYPE, [])

    def get_updated_record(self, original_record):
        original_record.name = "New Name"
        original_record.game_rules = GameRules("Updated Rules", False)
        original_record.home_pattern = [1, 2, 3, 5]

        return original_record

    def test_get_pattern_properly(self):
        session = self.setup_basic_test()
        rules = SeriesRules("Test", GameRules("Rules", True), SeriesRules.WINS_TYPE, [1, 5, 6, 7])
        self.get_repo().add(rules, session)
        session.commit()

        retrieved_object = self.get_repo().get_by_oid(rules.oid, session)

        self.assertEqual(1, retrieved_object.home_pattern[0])
        self.assertEqual(5, retrieved_object.home_pattern[1])
        self.assertEqual(6, retrieved_object.home_pattern[2])
        self.assertEqual(7, retrieved_object.home_pattern[3])
