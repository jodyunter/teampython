from unittest import TestCase

from teams.data.repo.configuration_repository import ConfigurationRepository
from teams.domain.gamedata import GameData
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestConfigurationRepository(TestBaseRepository, TestCase):
    repo = ConfigurationRepository()

    def test_add(self):
        session = self.setup_basic_test()
        game_data = GameData(5, 225)
        self.repo.add(game_data, session)
        session.commit()

        data = self.repo.get_all(session)
        self.assertEqual(2, len(data))

    def test_update(self):
        session = self.setup_basic_test()
        game_data = GameData(5, 225)
        self.repo.add(game_data, session)
        session.commit()

        game_data_u = GameData(66, 3465)
        self.repo.update(game_data_u, session)
        session.commit()

        game_data_r = self.repo.get_current_data(session)

        self.assertEqual(game_data_r.current_year, 66)
        self.assertEqual(game_data_r.current_day, 3465)

    def test_get(self):
        session = self.setup_basic_test()
        game_data = GameData(35, 1234)
        self.repo.add(game_data, session)
        session.commit()

        new_gd = self.repo.get_current_data(session)

        self.assertEqual(game_data.current_year, new_gd.current_year, "check year")
        self.assertEqual(game_data.current_day, new_gd.current_day, "check day")


