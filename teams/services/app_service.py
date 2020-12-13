from teams.data.repo.controller_repository import ControllerRepository
from teams.services.base_service import BaseService
from teams.services.view_models.controller_view_models import ControllerViewModel


class AppService(BaseService):
    repo = ControllerRepository()

    def get_current_data(self):
        session = self.get_session()
        dto = self.repo.get_current_data(session)
        return ControllerViewModel(dto.current_year, dto.current_day)
