class SeriesRules:
    WINS_TYPE = "ByWins"
    GOALS_TYPE = "ByGoals"

    def __init__(self, name, games, series_type):
        self.name = name
        self.games = games
        self.series_type = series_type


class SeriesByWinsRules(SeriesRules):

    def __init__(self, name, required_wins, home_team_pattern):
        self.home_team_pattern = home_team_pattern

        SeriesRules.__init__(name, required_wins, SeriesRules.WINS_TYPE)


class SeriesByGoals(SeriesRules):

    def __init__(self, name, games, last_game_rules):
        self.last_game_rules = last_game_rules

        SeriesRules.__init__(name, games, SeriesRules.GOALS_TYPE)
