from teams.data.repo.configuration_repository import ConfigurationRepository
from teams.domain.gamedata import GameData
from teams.services.base_service import BaseService
from teams.services.view_models.controller_view_models import GameDataViewModel


class AppService(BaseService):
    repo = ConfigurationRepository()

    def get_current_data(self):
        session = self.get_session()
        game_data = self.repo.get_current_data(session)
        return GameDataViewModel(game_data.current_year, game_data.current_day)

    def setup_data(self, year, day):
        session = self.get_session()
        game_data = GameData(year, day)
        self.repo.add(game_data, session)

    def change_day(self, new_day):
        session = self.get_session()
        game_data = self.repo.get_current_data(session)
        game_data.current_day = new_day
        session.commit()

    def change_year(self, new_year):
        session = self.get_session()
        dto = self.repo.get_current_data(session)
        dto.current_year = new_year
        session.commit()
