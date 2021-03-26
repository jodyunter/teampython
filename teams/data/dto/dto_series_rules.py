from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.series_rules import SeriesRules


# todo: create repo
class SeriesRulesDTO(Base, SeriesRules):
    __tablename__ = "seriesrules"

    oid = Column(String, primary_key=True)
    name = Column(String)
    game_rules_id = Column(String, ForeignKey('gamerules.oid'))
    game_rules = relationship("GameRulesDTO", foreign_keys=[game_rules_id])
    series_type = Column(String)
    home_pattern = Column(String)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'series_rules'
    }

    def __init__(self, series_rules):
        SeriesRules.__init__(self,
                             series_rules.name,
                             series_rules.game_rules,
                             series_rules.series_type,
                             series_rules.home_pattern,
                             series_rules.oid)