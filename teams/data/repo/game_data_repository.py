from teams.data.repo.repository import Repository
from teams.domain.gamedata import GameData


class GameDataRepository(Repository):

    def get_type(self):
        return GameData

    def get_current_data(self, session):
        return session.query(self.get_type()).first()




