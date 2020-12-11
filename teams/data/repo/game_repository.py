from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.base_repository import BaseRepository


class GameRepository(BaseRepository):
    def get_type(self):
        return GameDTO

    @staticmethod
    def add(game, session):
        game_dto = GameDTO(game)
        session.add(game_dto)
        pass

    def get_by_unprocessed_and_complete(self, session):
        return session.query(self.get_type()).filter_by(processed=False, complete=True)
