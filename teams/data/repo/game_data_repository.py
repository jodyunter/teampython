from teams.data.dto.dto_game_data import GameDataDTO
from teams.data.repo.repository import Repository


class GameDataRepository(Repository):

    @staticmethod
    def get_current_data(session):
        return session.query(GameDataDTO).first()




