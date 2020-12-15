class TeamViewModel:

    def __init__(self, oid, name, skill):
        self.name = name
        self.skill = skill
        self.oid = oid


class RecordViewModel:

    def __init__(self, oid, rank, team_id, team_name, year, wins, loses, ties, goals_for, goals_against, points, games,
                 goal_difference, skill):
        self.oid = oid
        self.rank = rank
        self.team_id = team_id
        self.team_name = team_name
        self.year = year
        self.wins = wins
        self.loses = loses
        self.ties = ties
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.points = points
        self.games = games
        self.goal_difference = goal_difference
        self.skill = skill
