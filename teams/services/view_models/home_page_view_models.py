class HomePageViewModel:

    def __init__(self, yesterday_games, games_view_list, current_data, standings_view, button_view):
        self.current_data = current_data
        self.yesterday_games = yesterday_games
        self.games = games_view_list
        self.records = standings_view.records
        self.buttons = button_view
        self.play_games_disabled = button_view.play_games_disabled
        self.setup_season_disabled = button_view.setup_season_disabled


class ButtonViewModel:

    #  when disabling in flask, you just add "disabled" otherwise have nothing
    def __init__(self, current_data):
        self.play_games_disabled = "disabled"
        self.setup_season_disabled = "disabled"

        if current_data.is_year_setup and current_data.is_year_finished:
            self.setup_season_disabled = ""
            self.play_games_disabled = "disabled"
        elif current_data.is_year_setup and not current_data.is_year_finished:
            self.play_games_disabled = ""
            self.setup_season_disabled = "disabled"
        elif not current_data.is_year_setup and not current_data.is_year_finished:
            self.play_games_disabled = "disabled"
            self.setup_season_disabled = ""

