from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.custom.custom_types import IntArrayString
from teams.data.dto.dto_base import Base
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.domain.series_rules import SeriesRules


class SeriesRulesDTO(Base, SeriesRules):
    __tablename__ = "seriesrules"

    oid = Column(String, primary_key=True)
    name = Column(String)
    game_rules_id = Column(String, ForeignKey('gamerules.oid'))
    game_rules = relationship("GameRulesDTO", foreign_keys=[game_rules_id])
    series_type = Column(String)
    home_pattern = Column(IntArrayString)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'series_rules'
    }

    def __init__(self, series_rules):
        rules = GameRulesDTO.get_dto(series_rules.game_rules)
        SeriesRules.__init__(self,
                             series_rules.name,
                             rules,
                             series_rules.series_type,
                             series_rules.home_pattern,
                             series_rules.oid)

    def __eq__(self, other):
        return self.name == other.name and \
            self.game_rules == other.game_rules and \
            self.series_type == other.series_type and \
            self.home_pattern == other.home_pattern and \
            self.oid == other.oid


    @staticmethod
    def get_dto(r):
        if r.__class__ == SeriesRulesDTO:
            return r
        else:
            return SeriesRulesDTO(r)
