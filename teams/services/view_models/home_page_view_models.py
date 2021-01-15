class HomePageViewModel:

    def __init__(self, games_view_list, current_data, standings_view):
        self.current_data = current_data
        self.games = games_view_list
        self.records = standings_view.records
