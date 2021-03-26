from teams.data.dto.dto_table_sub_competition import TableSubCompetitionDTO
from teams.data.repo.base_repository import BaseRepository


class TableSubCompetitionRepository(BaseRepository):
    def get_type(self):
        return TableSubCompetitionDTO