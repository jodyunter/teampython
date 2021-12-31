from unittest import TestCase

from teams.data.repo.game_data_repository import GameDataRepository
from teams.domain.gamedata import GameData
from tests.teams.repo.test_repository import BaseRepoTests


class GameDataRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return GameDataRepository()

    def test_add_record(self):
        pass

    def test_update_record(self):
        pass

    def get_add_record(self):
        return GameData("My Name", 5, 12, True, False)

    def get_updated_record(self, original_record):
        original_record.name = "New Name"
        original_record.current_year = 50
        original_record.current_day = 120
        original_record.is_year_setup = False
        original_record.is_year_finished = True

    def test_get(self):
        session = self.setup_basic_test()
        game_data = GameData("game_data", 35, 1234, True, False)
        session.add(game_data)
        session.commit()

        new_gd = self.get_repo().get_current_data(session)

        self.assertEqual(game_data.current_year, new_gd.current_year, "check year")
        self.assertEqual(game_data.current_day, new_gd.current_day, "check day")
        self.assertEqual(game_data.is_year_setup, new_gd.is_year_setup, "check year setup")
        self.assertEqual(game_data.is_year_finished, new_gd.is_year_finished, "check year finished")


