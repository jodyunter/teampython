from teams.domain.utility.utility_classes import IDHelper


class SeriesRules:
    WINS_TYPE = "ByWins"
    GOALS_TYPE = "ByGoals"

    def __init__(self, name, game_rules, series_type, oid=None):
        self.name = name
        self.series_type = series_type
        self.game_rules = game_rules
        self.oid = IDHelper.get_id(oid)


class SeriesByWinsRules(SeriesRules):

    def __init__(self, name, required_wins, game_rules, home_team_pattern, oid=None):
        self.home_team_pattern = home_team_pattern
        self.required_wins = required_wins

        SeriesRules.__init__(self, name, game_rules, SeriesRules.WINS_TYPE, oid)


class SeriesByGoalsRules(SeriesRules):

    # TODO: add home team pattern here too
    def __init__(self, name, games_to_play, game_rules, last_game_rules, oid=None):
        self.last_game_rules = last_game_rules
        self.games_to_play = games_to_play

        SeriesRules.__init__(self, name, game_rules, SeriesRules.GOALS_TYPE, oid)
