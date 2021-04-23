from unittest import TestCase

from teams.data.repo.game_data_repository import GameDataDTO, GameDataRepository
from teams.domain.gamedata import GameData
from tests.teams.repo.test_repository import TestBaseRepository


class TestGameDataRepository(TestBaseRepository, TestCase):

    def test_get(self):
        session = self.setup_basic_test()
        game_data = GameDataDTO(GameData("game_data", 35, 1234, True, False))
        session.add(game_data)
        session.commit()

        new_gd = GameDataRepository.get_current_data(session)

        self.assertEqual(game_data.current_year, new_gd.current_year, "check year")
        self.assertEqual(game_data.current_day, new_gd.current_day, "check day")
        self.assertEqual(game_data.is_year_setup, new_gd.is_year_setup, "check year setup")
        self.assertEqual(game_data.is_year_finished, new_gd.is_year_finished, "check year finished")


