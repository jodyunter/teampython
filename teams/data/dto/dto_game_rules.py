from sqlalchemy import Column, String, Integer

from teams.data.dto.dto_base import Base
from teams.domain.game import GameRules


class GameRulesDTO(Base, GameRules):
    __tablename__ = "gamerules"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    can_tie = Column(Integer)

    def __init__(self, game_rules):
        GameRules.__init__(self, game_rules.name, game_rules.can_tie, game_rules.oid)

    @staticmethod
    def get_dto(game_rules):
        if game_rules.__class__ == GameRulesDTO:
            return game_rules
        else:
            return GameRulesDTO(game_rules)