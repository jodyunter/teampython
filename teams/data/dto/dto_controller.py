from sqlalchemy import Column, Integer

from teams.data.dto.dto_base import Base
from teams.domain.controller import Controller


class ControllerDTO(Base, Controller):
    __tablename__ = "controller"

    current_day = Column(Integer)
    current_year = Column(Integer)

    def __init__(self, controller):
        Controller.__init__(self, controller.current_year, controller.current_day)
