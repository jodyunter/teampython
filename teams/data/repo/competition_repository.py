from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.repo.base_repository import BaseRepository


# todo: use this pattern and put the add in the base repo class
class CompetitionRepository(BaseRepository):
    def add(self, new_object, session):
        dto = self.get_type()(new_object)
        session.add(dto)

    def get_type(self):
        return CompetitionDTO
