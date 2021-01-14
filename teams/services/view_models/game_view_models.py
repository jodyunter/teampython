class GameRulesViewModel:
    def __init__(self, oid, name, can_tie):
        self.oid = oid
        self.name = name
        self.can_tie = can_tie


class GameViewModel:

    def __init__(self, oid, year, day, home_name, home_id, away_name, away_id, home_score, away_score, status):
        self.oid = oid
        self.year = year
        self.day = day
        self.home_name = home_name
        self.home_id = home_id
        self.away_name = away_name
        self.away_id = away_id
        self.home_score = home_score
        self.away_score = away_score
        self.status = status


class GameDayViewModel:

    def __init__(self, current_data_view, day_viewing, year_viewing, game_view_list):
        self.current_data = current_data_view
        self.day = day_viewing
        self.year = year_viewing
        self.games = game_view_list
