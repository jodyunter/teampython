from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_playoff_sub_competition import PlayoffSubCompetitionDTO
from teams.data.dto.dto_sub_competition import SubCompetitionDTO
from teams.data.dto.dto_table_sub_competition import TableSubCompetitionDTO
from teams.data.repo.repository import Repository


class CompetitionRepository(Repository):

    def get_type(self):
        return CompetitionDTO


class SubCompetitionRepository(Repository):

    def get_type(self):
        return SubCompetitionDTO


class TableSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return TableSubCompetitionDTO


class PlayoffSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return PlayoffSubCompetitionDTO
