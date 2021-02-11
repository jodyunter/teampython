class SeriesViewModel:

    def __init__(self, name, year, round, game_vms, team1_vm, team1_wins, team2_vm, team2_wins, status):
        self.name = name
        self.round = round
        self.year = year
        self.games = game_vms
        self.team1 = team1_vm
        self.team2 = team2_vm
        self.team1_wins = team1_wins
        self.team2_wins = team2_wins
        self.status = status
