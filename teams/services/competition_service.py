from teams.data.repo.competition_repository import CompetitionRepository
from teams.services.base_service import BaseService


class CompetitionService(BaseService):
    repo = CompetitionRepository()

    def get_repo(self):
        return self.repo




