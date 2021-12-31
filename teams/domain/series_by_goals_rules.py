from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain.series_rules import SeriesRules


class SeriesByGoalsRules(SeriesRules):
    games_to_play = Column(Integer)
    last_game_rules_id = Column(String, ForeignKey('gamerules.oid'))
    last_game_rules = relationship("GameRules", foreign_keys=[last_game_rules_id])

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins'
    }

    def __init__(self, name, games_to_play, game_rules, last_game_rules, home_pattern, oid=None):
        self.last_game_rules = last_game_rules
        self.games_to_play = games_to_play

        SeriesRules.__init__(self, name, game_rules, SeriesRules.GOALS_TYPE, home_pattern, oid)
