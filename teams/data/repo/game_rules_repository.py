from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.repo.repository import Repository


class GameRulesRepository(Repository):

    @staticmethod
    def get_by_name(name, session):
        return session.query(GameRulesDTO).filter_by(name=name).first()
