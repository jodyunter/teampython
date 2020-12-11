class Record:

    def __init__(self, team, year, wins, loses, ties, goals_for, goals_against, oid):
        self.oid = oid
        self.team = team
        self.year = year
        self.wins = wins
        self.loses = loses
        self.ties = ties
        self.goals_for = goals_for
        self.goals_against = goals_against

    @property
    def points(self):
        return self.wins * 2 + self.ties

    @property
    def games(self):
        return self.wins + self.ties + self.loses

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    def process_game(self, us, them):
        if us == them:
            self.ties += 1
        elif us > them:
            self.wins += 1
        else:
            self.loses += 1

        self.goals_for += us
        self.goals_against += them