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

    def play(self, random):
        if not self.complete:
            self.home_score = random.randint(0, 6)
            self.away_score = random.randint(0, 6)
            while self.home_score == self.away_score and self.rules.can_tie:
                a = random.randint(-6, 6)
                if a < 0:
                    self.away_score += 1
                elif a > 0:
                    self.home_score += 1

            self.complete = True

