class GameViewModel:
    def __init__(self, oid, year, day, home_name, home_id, away_name, away_id, home_score, away_score, status):
        self.oid = oid
        self.year = year
        self.day = day
        self.home_name = home_name
        self.home_id = home_id
        self.away_name = away_name
        self.away_id = away_id
        self.home_score = home_score
        self.away_score = away_score
        self.status = status
