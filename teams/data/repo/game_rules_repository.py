from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.repo.base_repository import BaseRepository


class GameRulesRepository(BaseRepository):
    def get_type(self):
        return GameRulesDTO

    def add(self, game_rules, session):
        dto = GameRulesDTO.get_dto(game_rules)
        session.add(dto);
        session.commit()


