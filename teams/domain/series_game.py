from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from teams.domain.competition_game import CompetitionGame


class SeriesGame(CompetitionGame):
    series_id = Column(String, ForeignKey('series.oid'))
    series = relationship('Series', foreign_keys=[series_id])
    game_number = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_game'
    }

    def __init__(self, series, game_number, competition, sub_competition, day, home_team, away_team, home_score,
                 away_score, complete, processed,
                 rules, oid=None):
        self.series = series
        self.game_number = game_number

        CompetitionGame.__init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score,
                                 complete, processed,
                                 rules, oid)