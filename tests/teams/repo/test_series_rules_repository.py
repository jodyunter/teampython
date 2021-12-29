from unittest import TestCase

from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_series_rules import SeriesRulesDTO
from teams.data.repo.rules_repository import SeriesRulesRepository, GameRulesRepository
from teams.domain.game import GameRules
from teams.domain.series_rules import SeriesRules
from tests.teams.repo.test_repository import BaseRepoTests


class TestSeriesRulesRepository(BaseRepoTests, TestCase):
    def get_repo(self):
        return SeriesRulesRepository()

    def get_game_rules_repo(self):
        return GameRulesRepository()

    def get_add_record(self):
        return SeriesRulesDTO(SeriesRules("Test Rule", GameRules("My Rules", False), SeriesRules.WINS_TYPE, []))

    def get_updated_record(self, original_record):
        original_record.name = "New Name"
        original_record.game_rules = GameRulesDTO(GameRules("Updated Rules", False))
        original_record.home_pattern = [1, 2, 3, 5]

        return original_record

    def test_get_pattern_properly(self):
        session = self.setup_basic_test()
        rules = SeriesRules("Test", GameRules("Rules", True), SeriesRules.WINS_TYPE, [1, 5, 6, 7])
        self.get_repo().add(SeriesRulesDTO(rules), session)
        session.commit()

        retrieved_object = self.get_repo().get_by_oid(rules.oid, session)

        self.assertEqual(1, retrieved_object.home_pattern[0])
        self.assertEqual(5, retrieved_object.home_pattern[1])
        self.assertEqual(6, retrieved_object.home_pattern[2])
        self.assertEqual(7, retrieved_object.home_pattern[3])
