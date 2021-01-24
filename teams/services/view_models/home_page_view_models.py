class HomePageViewModel:

    def __init__(self, map_of_games_by_day, current_data, standings_view, button_view, active_day):
        self.current_data = current_data
        self.days = map_of_games_by_day
        self.standings_view = standings_view
        self.buttons_view = button_view
        self.active_day = active_day


    def getDaysInReverseOrder(self):
        return sorted(self.days, reverse=True)


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

