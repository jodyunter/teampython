class SeriesRules:
    WINS_TYPE = "ByWins"
    GOALS_TYPE = "ByGoals"

    def __init__(self, name, series_type):
        self.name = name
        self.series_type = series_type


class SeriesByWinsRules(SeriesRules):

    def __init__(self, name, required_wins, home_team_pattern):
        self.home_team_pattern = home_team_pattern
        self.required_wins = required_wins

        SeriesRules.__init__(self, name, SeriesRules.WINS_TYPE)


class SeriesByGoalsRules(SeriesRules):

    def __init__(self, name, games_to_play, last_game_rules):
        self.last_game_rules = last_game_rules
        self.games_to_play = games_to_play

        SeriesRules.__init__(self, name, SeriesRules.GOALS_TYPE)
