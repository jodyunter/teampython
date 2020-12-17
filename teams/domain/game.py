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

    score_matrix = [
        [0, 0, 500],
        [1, 500, 1500],
        [2, 1500, 4000],
        [3, 4000, 9000],
        [4, 9000, 14000],
        [5, 14000, 16500],
        [6, 16500, 17500],
        [7, 17500, 17750],
        [8, 17750, 17875],
        [9, 17875, 17950],
        [10, 17950, 17975],
    ]

    def get_score(self, skill_diff, random):
        if skill_diff < -20 or skill_diff > 10:
            raise ValueError(str(skill_diff) + " is not a valid skill difference.")

        min_value = 0
        max_value = 17975 - 1
        modifier = skill_diff * 1000

        value = random.randint(min_value + modifier, max_value)
        #print(str(skill_diff) + " : " + str(modifier) + " : " + str(value))
        if value < 0:
            return 0

        for a in self.score_matrix:
            possible_score = a[0]
            if a[1] <= value < a[2]:
                return possible_score

        raise ValueError("Matrix didn't have a value.")

    def play(self, random):
        if not self.complete:
            skill_diff = self.home_team.skill - self.away_team.skill

            self.home_score = self.get_score(skill_diff, random)
            self.away_score = self.get_score(skill_diff * -1, random)
            while self.home_score == self.away_score and not self.rules.can_tie:
                a = random.randint(-6, 6)
                if a < 0:
                    self.away_score += 1
                elif a > 0:
                    self.home_score += 1

            self.complete = True
