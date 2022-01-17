from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from teams.data.dto.custom.custom_types import IntArrayString
from teams.domain.base import Base
from teams.domain.utility.utility_classes import IDHelper


class SeriesRules(Base):
    __tablename__ = "SeriesRules"

    oid = Column(String, primary_key=True)
    name = Column(String)
    game_rules_id = Column(String, ForeignKey('GameRules.oid'))
    game_rules = relationship("GameRules", foreign_keys=[game_rules_id])
    series_type = Column(String)
    home_pattern = Column(IntArrayString)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'series_rules'
    }

    WINS_TYPE = "ByWins"
    GOALS_TYPE = "ByGoals"

    def __init__(self, name, game_rules, series_type, home_pattern, oid=None):
        self.name = name
        self.series_type = series_type
        self.game_rules = game_rules
        self.home_pattern = home_pattern
        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
            self.oid = oid

