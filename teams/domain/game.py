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
        [1, 500, 1250],
        [2, 1250, 2250],
        [3, 2250, 3250],
        [4, 3250, 4250],
        [5, 4250, 5250],
        [6, 5250, 6000],
        [7, 6000, 6500],
        [8, 6500, 6750],
        [9, 6750, 6875],
        [10, 6875, 6950],
        [11, 6950, 7000],
        [12, 7000, 7025],
        [13, 7025, 7045],
        [14, 7045, 7060],
        [15, 7060, 7070],
        [16, 7070, 7077],
        [17, 7077, 7082],
        [18, 7082, 7085],
        [19, 7085, 7087],
        [20, 7087, 7088]
    ]

    def get_score(self, skill_diff, random):
        if skill_diff < -20 or skill_diff > 10:
            raise ValueError(str(skill_diff) + " is not a valid skill difference.")

        min_value = 0
        max_value = 7088 - 1
        modifier = skill_diff * 100

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
