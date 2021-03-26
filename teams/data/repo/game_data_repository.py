from teams.data.dto.dto_game_data import GameDataDTO
from teams.data.repo.base_repository import BaseRepository


class GameDataRepository(BaseRepository):
    def get_type(self):
        return GameDataDTO;

    def get_current_data(self, session):
        return session.query(self.get_type()).first()




