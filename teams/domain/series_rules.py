class SeriesRules:

    def __init__(self, name, games):
        self.name = name
        self.games = games


class SeriesByWinsRules(SeriesRules):

    def __init__(self, name, required_wins, home_team_pattern):
        self.home_team_pattern = home_team_pattern

        super(SeriesRules).__init__(name, required_wins)


class SeriesByGoals(SeriesRules):

    def __init__(self, name, games, last_game_rules):
        self.last_game_rules = last_game_rules

        super(SeriesRules).__init__(name, games)
