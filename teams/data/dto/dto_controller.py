from sqlalchemy import Column, Integer, String

from teams.data.dto.dto_base import Base
from teams.domain.controller import Controller


class ControllerDTO(Base, Controller):
    __tablename__ = "controller"

    oid = Column(String, primary_key=True)
    current_day = Column(Integer)
    current_year = Column(Integer)

    def __init__(self, controller):
        Controller.__init__(self, oid, controller.current_year, controller.current_day)
