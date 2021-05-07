from sqlalchemy import Column, String, Boolean

from teams.data.dto.dto_base import Base
from teams.domain.game import GameRules


class GameRulesDTO(Base, GameRules):
    __tablename__ = "gamerules"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    can_tie = Column(Boolean)

    def __init__(self, game_rules):
        GameRules.__init__(self, game_rules.name, game_rules.can_tie, game_rules.oid)

    def __eq__(self, other):
        return self.name == other.name and self.can_tie == other.can_tie and self.oid == other.oid

    @staticmethod
    def get_dto(game_rules):
        if game_rules.__class__ == GameRulesDTO:
            return game_rules
        else:
            return GameRulesDTO(game_rules)
