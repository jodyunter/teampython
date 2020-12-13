from teams.data.dto.dto_controller import ControllerDTO
from teams.data.repo.base_repository import BaseRepository


class ControllerRepository(BaseRepository):
    def get_type(self):
        ControllerDTO

    def get_current_data(self, session):
        return session.query(self.get_type()).first()
