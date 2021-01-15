from unittest import TestCase

from teams.services.view_models.app_view_models import GameDataViewModel
from teams.services.view_models.home_page_view_models import ButtonViewModel


class TestButtonViewModel(TestCase):

    def test_should_set_buttons_not_setup_and_not_finished(self):
        current_data = GameDataViewModel(5, 25, False, False)
        button_model = ButtonViewModel(current_data)
        self.assertEqual(button_model.play_games_disabled, "disabled")
        self.assertEqual(button_model.setup_season_disabled, "")

    def test_should_set_buttons_not_setup_and_finished(self):
        current_data = GameDataViewModel(5, 25, False, True)
        button_model = ButtonViewModel(current_data)
        self.assertEqual(button_model.play_games_disabled, "disabled")
        self.assertEqual(button_model.setup_season_disabled, "disabled")

    def test_should_set_buttons_setup_and_not_finished(self):
        current_data = GameDataViewModel(5, 25, True, False)
        button_model = ButtonViewModel(current_data)
        self.assertEqual(button_model.play_games_disabled, "")
        self.assertEqual(button_model.setup_season_disabled, "disabled")

    def test_should_set_buttons_setup_and_finished(self):
        current_data = GameDataViewModel(5, 25, True, True)
        button_model = ButtonViewModel(current_data)
        self.assertEqual(button_model.play_games_disabled, "disabled")
        self.assertEqual(button_model.setup_season_disabled, "")