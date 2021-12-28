from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.repo.repository import Repository


class GameRulesRepository(Repository):

    def get_type(self):
        return GameRulesDTO

    def get_by_name(self, name, session):
        return session.query(GameRulesDTO).filter_by(name=name).first()
