from teams.data.dto.dto_configuration import ConfigurationItemDTO
from teams.data.repo.base_repository import BaseRepository
from teams.domain.gamedata import GameData, ConfigurationItem


class ConfigurationRepository(BaseRepository):
    def get_type(self):
        return ConfigurationItemDTO

    def get_current_data(self, session):
        year = session.query(self.get_type()).filter_by(name=GameData.current_year_string).first()
        day = session.query(self.get_type()).filter_by(name=GameData.current_day_string).first()

        return GameData(year.data, day.data)

    @staticmethod
    def add(configuration, session):
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.current_year_string, configuration.current_year)))
        session.add(
            ConfigurationItemDTO(ConfigurationItem(GameData.current_day_string, configuration.current_day)))

    def update(self, configuration, session):
        dto_cy = session.query(self.get_type()).filter_by(name=GameData.current_year_string).first()
        dto_cd = session.query(self.get_type()).filter_by(name=GameData.current_day_string).first()

        dto_cy.data = configuration.current_year
        dto_cd.data = configuration.current_day

        session.commit()
