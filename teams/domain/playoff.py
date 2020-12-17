class PlayoffSeriesRules:
    def __init__(self, po_round, required_wins, game_rules, team1_from, team2_from):
        self.po_round = po_round
        self.required_wins = required_wins
        self.game_rules = game_rules
        self.team1_from = team1_from
        self.team2_from = team2_from


class PlayoffSeries:

    def __init__(self, year, team1, team2, po_series_rules, games_list, setup, complete):
        self.year = year
        self.team1 = team1
        self.team2 = team2
        if games_list is None:
            games_list = []
        self.games = games_list
        self.rules = po_series_rules
        self.setup = setup
        self.complete = complete

    def setup(self, playoff):
        pass

