from teams.data.dto.dto_configuration import ConfigurationItemDTO
from teams.data.repo.base_repository import BaseRepository
from teams.domain.gamedata import GameData, ConfigurationItem
from teams.services.view_models.controller_view_models import GameDataViewModel


class ConfigurationRepository(BaseRepository):
    def get_type(self):
        return ConfigurationItemDTO

    def get_current_data(self, session):
        year = session.query(self.get_type()).filter_by(name=GameData.current_year_string).first()
        day = session.query(self.get_type()).filter_by(name=GameData.current_day_string).first()
        year_setup = session.query(self.get_type()).filter_by(name=GameData.is_year_setup_string).first()
        year_finished = session.query(self.get_type()).filter_by(name=GameData.is_year_finished_string).first()
        return GameDataViewModel(year.data, day.data, year_setup.data, year_finished.data)

    @staticmethod
    def add(configuration, session):
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.current_year_string, configuration.current_year)))
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.current_day_string, configuration.current_day)))
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.is_year_setup_string, configuration.is_year_setup)))
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.is_year_finished_string, configuration.is_year_finished)))

    def update(self, configuration, session):
        dto_cy = session.query(self.get_type()).filter_by(name=GameData.current_year_string).first()
        dto_cd = session.query(self.get_type()).filter_by(name=GameData.current_day_string).first()
        dto_ys = session.query(self.get_type()).filter_by(name=GameData.is_year_setup_string).first()
        dto_yf = session.query(self.get_type()).filter_by(name=GameData.is_year_finished_string).first()

        dto_cy.data = configuration.current_year
        dto_cd.data = configuration.current_day
        dto_ys.data = configuration.is_year_setup
        dto_yf.data = configuration.is_year_finished

