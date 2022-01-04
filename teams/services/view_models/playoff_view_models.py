class SeriesViewModel:

    def __init__(self, oid, name, year, series_round, game_vms, team1_vm, team1_wins, team2_vm, team2_wins, status):
        self.oid = oid
        self.name = name
        self.round = series_round
        self.year = year
        self.games = game_vms
        self.team1 = team1_vm
        self.team2 = team2_vm
        self.team1_wins = team1_wins
        self.team2_wins = team2_wins
        self.status = status


class SeriesByWinsRulesViewModel:

    def __init__(self, oid, name, required_wins, game_rules_vm, home_pattern):
        self.oid = oid
        self.name = name
        self.required_wins = required_wins
        self.game_rules = game_rules_vm
        self.home_pattern = home_pattern


class SeriesByGoalsRulesViewModel:
    def __init__(self, oid, name, games_to_play, game_rules_vm, last_game_rules_vm, home_pattern):
        self.oid = oid
        self.name = name
        self.games_to_play = games_to_play
        self.game_rules = game_rules_vm
        self.last_game_rules = last_game_rules_vm
        self.home_pattern = home_pattern
