import numpy as np
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from teams.domain.base import Base
from teams.domain.utility.utility_classes import IDHelper
from teams.domain.game_rules import GameRules


# mapped
class Game(Base):
    __tablename__ = "games"

    oid = Column(String, primary_key=True)
    year = Column(Integer)
    day = Column(Integer)
    home_score = Column(Integer)
    away_score = Column(Integer)
    complete = Column(Boolean)
    processed = Column(Boolean)
    home_team_id = Column(String, ForeignKey('teams.oid'))
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team_id = Column(String, ForeignKey('teams.oid'))
    away_team = relationship("Team", foreign_keys=[away_team_id])
    rules_id = Column(String, ForeignKey('gamerules.oid'))
    rules = relationship("GameRules", foreign_keys=[rules_id])
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'game'
    }

    def __init__(self, year, day, home_team, away_team, home_score, away_score, complete, processed, rules, oid=None):
        self.year = year
        self.day = day
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.complete = complete
        self.oid = IDHelper.get_id(oid)
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

    def get_score(self, skill_diff):
        total_diff = skill_diff * 0.03
        if total_diff < 0:
            total_diff = 0
        elif total_diff >= 1:
            total_diff = 0.999

        n, p = 12, .25 + total_diff  # mean and standard deviation
        score = int(np.round(np.random.binomial(n, p, 1)))

        if score < 0:
            return 0
        else:
            return score

        raise ValueError("Matrix didn't have a value.")

    def play(self):
        if not self.complete:
            skill_diff = self.home_team.skill - self.away_team.skill

            self.home_score = self.get_score(skill_diff)
            self.away_score = self.get_score(skill_diff * -1)
            while self.home_score == self.away_score and not self.rules.can_tie:
                a = np.random.randint(-6, 6)
                if a < 0:
                    self.away_score += 1
                elif a > 0:
                    self.home_score += 1

            self.complete = True

    def get_winner(self):
        if self.complete:
            if self.home_score > self.away_score:
                return self.home_team
            elif self.away_score > self.home_score:
                return self.away_team

        return None

    def get_loser(self):
        if self.complete:
            if self.home_score < self.away_score:
                return self.home_team
            elif self.away_score < self.home_score:
                return self.away_team

        return None

    def __eq__(self, other):
        return self.oid == other.oid and \
               self.year == other.year and \
               self.day == other.day and \
               self.home_team == other.home_team and \
               self.away_team == other.away_team and \
               self.home_score == other.home_score and \
               self.away_score == other.away_score and \
               self.complete == other.complete and \
               self.processed == other.processed and \
               self.rules == other.rules
