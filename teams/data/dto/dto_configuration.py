from sqlalchemy import Column, Integer, String

from teams.data.dto.dto_base import Base
from teams.domain.gamedata import ConfigurationItem


class ConfigurationItemDTO(Base, ConfigurationItem):
    __tablename__ = "configuration"

    name = Column(String, primary_key=True)
    data = Column(Integer)

    def __init__(self, controller):
        ConfigurationItem.__init__(self, controller.name, controller.data)
