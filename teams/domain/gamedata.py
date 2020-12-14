class ConfigurationItem:

    def __init__(self, name, data):
        self.name = name
        self.data = data


class GameData:
    current_year_string = "Current Year"
    current_day_string = "Current Day"

    def __init__(self, current_year, current_day):
        self.current_year = current_year
        self.current_day = current_day
