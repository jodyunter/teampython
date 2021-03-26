from sqlalchemy import Column, Integer

from teams.data.dto.dto_series_rules import SeriesRulesDTO
from teams.domain.series_rules import SeriesByWinsRules


class SeriesByWinsRulesDTO(SeriesRulesDTO, SeriesByWinsRules):
    required_wins = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins'
    }

    def __init__(self, series_by_wins_rules):

        SeriesByWinsRules.__init__(self,
                                   series_by_wins_rules.name,
                                   series_by_wins_rules.required_wins,
                                   series_by_wins_rules.game_rules,
                                   series_by_wins_rules.home_pattern,
                                   series_by_wins_rules.oid)