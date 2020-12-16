class GameRules:
    def __init__(self, name, can_tie, oid):
        self.oid = oid
        self.name = name
        self.can_tie = can_tie


class Game:
    def __init__(self, year, day, home_team, away_team, home_score, away_score, complete, processed, rules, oid):
        self.year = year
        self.day = day
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.complete = complete
        self.oid = oid
        self.rules = rules
        self.processed = processed

    # one way that may save processing power is to have all matrices from -20 to +20 created by hand or in properties
    skill_value = 1000
    score_matrix = [[0, 0, 7500], [1, 7501, 32501], [2, 32502, 67502], [3, 67503, 92503], [4, 92504, 112504],
                    [5, 112505, 127505], [6, 127506, 140006], [7, 140007, 141007], [8, 141008, 141508],
                    [9, 141509, 141559], [10, 141560, 141585], [11, 141586, 141606], [12, 141607, 141617],
                    [13, 141618, 141623], [14, 141624, 141627], [15, 141628, 141629]]
    score_increments = [7500, 25000, 35000, 25000, 20000, 15000, 12500, 1000, 500, 50, 25, 20, 10, 5, 3, 1]

    change_matrix = [-10, -5, 0, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 10, 10]
    max_skill = 15

    def get_score(self, skill_diff, random):
        copy_inc = self.score_increments.copy()
        score_matrix = []
        for i in range(self.max_skill):
            multiplier = (1 + self.change_matrix[a[0]] / 100 * skill_diff)

        copy_matrix = self.score_matrix[:]
        for a in copy_matrix:
            multiplier = (1 + self.change_matrix[a[0]] / 100 * skill_diff)
            a[1] = int(a[1] * multiplier)
            a[2] = int(a[2] * multiplier)

            print(copy_matrix[a[0]])
            print(self.score_matrix[a[0]])

        random_value = random.randint(copy_matrix[0][1], copy_matrix[self.max_skill][2])

        for a in copy_matrix:
            possible_score = a[0]
            range_low = a[1]
            range_high = a[2]

            if range_low <= random_value <= range_high:
                return possible_score

    def play(self, random):
        if not self.complete:
            skill_diff = self.home_team.skill - self.away_team.skill

            self.home_score = self.get_score(skill_diff, random)
            self.away_score = self.get_score(skill_diff, random)
            while self.home_score == self.away_score and not self.rules.can_tie:
                a = random.randint(-6, 6)
                if a < 0:
                    self.away_score += 1
                elif a > 0:
                    self.home_score += 1

            self.complete = True
