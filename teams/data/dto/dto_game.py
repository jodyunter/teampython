from sqlalchemy import String, Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_team import TeamDTO
from teams.domain.game import Game


class GameDTO(Base, Game):
    __tablename__ = "games"

    oid = Column(String, primary_key=True)
    year = Column(Integer)
    day = Column(Integer)
    home_score = Column(Integer)
    away_score = Column(Integer)
    complete = Column(Boolean)
    processed = Column(Boolean)
    home_team_id = Column(String, ForeignKey('teams.oid'))
    home_team = relationship("TeamDTO", foreign_keys=[home_team_id])
    away_team_id = Column(String, ForeignKey('teams.oid'))
    away_team = relationship("TeamDTO", foreign_keys=[away_team_id])
    rules_id = Column(String, ForeignKey('gamerules.oid'))
    rules = relationship("GameRulesDTO", foreign_keys=[rules_id])

    def __init__(self, game):
        home_team_dto = TeamDTO.get_dto(game.home_team)
        away_team_dto = TeamDTO.get_dto(game.away_team)
        game_rules_dto = GameRulesDTO.get_dto(game.rules)

        Game.__init__(self, game.year, game.day, home_team_dto, away_team_dto,
                      game.home_score, game.away_score, game.complete, game.processed,
                      game_rules_dto, game.oid)
