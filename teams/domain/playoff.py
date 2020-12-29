class PlayoffSeriesRules:
    SERIES = "SERIES"
    WINNER = "WINNER"
    LOSER = "LOSER"
    STANDINGS = "RANKING"
    # FROM should be series or ranking
    # VALUE should be WINNER, LOSER or name of the ranking
    # RANK should be the number of the ranking

    def __init__(self, po_round, required_wins, game_rules, team1_from, team1_value, team1_rank, team2_from, team2_value, team2_rank):
        self.po_round = po_round
        self.required_wins = required_wins
        self.game_rules = game_rules
        self.team1_from = team1_from
        self.team1_rank = team1_rank
        self.team1_value = team1_value
        self.team2_from = team2_from
        self.team2_rank = team2_rank
        self.team2_value = team2_value


class PlayoffSeries:

    def __init__(self, year, team1, team2, team1_wins, team2_wins, po_series_rules, games_list, setup, complete):
        self.year = year
        self.team1 = team1
        self.team2 = team2
        self.team1_wins = team1_wins
        self.team2_wins = team2_wins
        if games_list is None:
            games_list = []
        self.games = games_list
        self.rules = po_series_rules
        self.setup = setup
        self.complete = complete

    def setup(self, playoff):
        pass

    def check_complete(self):
        required_wins = self.rules.required_wins

        if self.team1_wins == required_wins or self.team2_wins == required_wins:
            return True
        else:
            self.team1_wins = self.get_wins_for_team(self.team1)
            self.team2_wins = self.get_wins_for_team(self.team2)

            return self.team1_wins == required_wins or self.team2_wins == required_wins

    def get_wins_for_team(self, team):
        return [a.get_winner().oid == team.oid for a in self.game_list].count()

    def process_game(self, game_to_process):
        add_game_to_list = [game_to_process.oid == a.oid for a in self.game_list].count() == 0
        if add_game_to_list:
            self.game_list.append(game_to_process)

        if not game_to_process.processed:
            if game_to_process.complete:
                winner = game_to_process.get_winner()
                if winner.oid == self.team1.oid:
                    self.team1_wins += 1
                elif winner.oid == self.team2.oid:
                    self.team2_wins += 1

        if self.check_complete():
            self.complete = True

    def setup_game(self):
        pass



