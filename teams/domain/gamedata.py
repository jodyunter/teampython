class ConfigurationItem:

    def __init__(self, name, data):
        self.name = name
        self.data = data


class GameData:
    current_year_string = "Current Year"
    current_day_string = "Current Day"
    is_year_setup_string = "Is Current Year Setup"
    is_year_finished_string = "Is Current Year Finished"

    def __init__(self, current_year, current_day, is_year_setup, is_year_finished):
        self.current_year = current_year
        self.current_day = current_day
        self.is_year_setup = is_year_setup
        self.is_year_finished = is_year_finished
