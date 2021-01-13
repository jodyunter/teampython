
class StandingsHistoryViewModel:

    def __init__(self, current_data_view, year_viewing, records_view_list, season_list):
        self.current_data = current_data_view
        self.year = year_viewing
        self.records = records_view_list
        self.seasons = season_list


class StandingsCurrentViewModel:

    def __init__(self, current_data_view, records_view_list):
        self.current_data = current_data_view
        self.records = records_view_list