from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from teams.data.dto.dto_series_rules import SeriesRulesDTO
from teams.domain.series_rules import SeriesByGoalsRules


class SeriesByGoalsRulesDTO(SeriesRulesDTO, SeriesByGoalsRules):
    games_to_play = Column(Integer)
    last_game_rules_id = Column(String, ForeignKey('gamerules.oid'))
    last_game_rules = relationship("GameRulesDTO", foreign_key=[last_game_rules_id])

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins'
    }

    def __init__(self, series_by_goals_rules):

        SeriesByGoalsRules.__init__(self,
                                    series_by_goals_rules.name,
                                    series_by_goals_rules.games_to_play,
                                    series_by_goals_rules.game_rules,
                                    series_by_goals_rules.last_game_rules,
                                    series_by_goals_rules.home_pattern,
                                    series_by_goals_rules.oid)