from teams.data.repo.repository import Repository
from teams.domain.record import Record
from teams.domain.table_record import TableRecord


class RecordRepository(Repository):
    def get_type(self):
        return Record

    def get_by_year(self, year, session):
        return session.query(Record).filter_by(year=year)

    def get_by_team_and_year(self, team_id, year, session):
        return session.query(Record).filter_by(year=year, team_id=team_id).first()

    def get_by_team(self, team_id, session):
        return session.query(Record).filter_by(team_id=team_id)

    def get_by_rank(self, rank, session):
        return session.query(Record).filter_by(rank=rank)

    def get_list_of_seasons(self, session):
        return session.query(Record.year).distinct()


class TableRecordRepository(RecordRepository):

    def get_type(self):
        return TableRecord


