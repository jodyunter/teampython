from teams.data.repo.repository import Repository
from teams.domain.competition import Competition
from teams.domain.sub_competition import SubCompetition
from teams.domain.table_sub_competition import TableSubCompetition
from teams.domain.playoff_sub_competition import PlayoffSubCompetition


class CompetitionRepository(Repository):

    def get_type(self):
        return Competition

    def get_by_year(self, year, session):
        dto_type = self.get_type()

        return session.query(dto_type).filter(dto_type.year == year)

    def get_by_year_and_status(self, setup, started, finished, post_processed, session):

        dto_type = self.get_type()

        return session.query(dto_type).filter(dto_type.setup == setup, dto_type.finished == finished,
                                              dto_type.post_processed == post_processed,
                                              dto_type.started == started)


class SubCompetitionRepository(Repository):

    def get_type(self):
        return SubCompetition


class TableSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return TableSubCompetition


class PlayoffSubCompetitionRepository(SubCompetitionRepository):

    def get_type(self):
        return PlayoffSubCompetition
