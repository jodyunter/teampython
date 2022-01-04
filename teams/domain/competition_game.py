
# mapped
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from teams.domain.game import Game


class CompetitionGame(Game):
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("SubCompetition", foreign_keys=[sub_competition_id])
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("Competition", foreign_keys=[competition_id])

    __mapper_args__ = {
        'polymorphic_identity': 'competition_game'
    }

    def __init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete,
                 game_processed, rules, oid=None):
        self.sub_competition = sub_competition
        self.competition = competition

        Game.__init__(self, competition.year, day, home_team, away_team, home_score, away_score, complete,
                      game_processed, rules,
                      oid)
