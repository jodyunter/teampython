from teams.data.dto.dto_game_data import GameDataDTO
from teams.data.repo.repository import Repository


class GameDataRepository(Repository):

    def get_current_data(self, session):
        return session.query(GameDataDTO).first()




