from teams.domain.utility.utility_classes import IDHelper

# mapped
class Record:

    def __init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid=None):
        self.oid = IDHelper.get_id(oid)
        self.rank = rank
        self.team = team
        self.year = year
        self.wins = wins
        self.loses = loses
        self.ties = ties
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.skill = skill

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

    @staticmethod
    def sort_records_default(records):
        rank = 1
        records.sort(key=lambda rec: (-rec.points, -rec.wins, rec.games, -rec.goal_difference))
        for r in records:
            r.rank = rank
            rank += 1
