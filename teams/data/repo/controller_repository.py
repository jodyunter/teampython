from teams.data.dto.dto_controller import ControllerDTO
from teams.data.repo.base_repository import BaseRepository


class ControllerRepository(BaseRepository):
    def get_type(self):
        ControllerDTO

    def get_current_data(self, session):
        return session.query(self.get_type()).first()

    def add(self, controller, session):
        dto = session.query(self.get_type()).first()
        if dto is None:
            dto = ControllerDTO(1, 1)

        dto = ControllerDTO(controller.current_year, controller.current_day)

        session.add(dto)

