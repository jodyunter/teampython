from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.repository import Repository
from teams.data.repo.team_repository import TeamRepository


class RecordRepository(Repository):
    def get_type(self):
        return RecordDTO

    def get_by_year(self, year, session):
        return session.query(RecordDTO).filter_by(year=year)

    def get_by_team_and_year(self, team_id, year, session):
        return session.query(RecordDTO).filter_by(year=year, team_id=team_id).first()

    def get_by_team(self, team_id, session):
        return session.query(RecordDTO).filter_by(team_id=team_id)

    def get_by_rank(self, rank, session):
        return session.query(RecordDTO).filter_by(rank=rank)

    def get_list_of_seasons(self, session):
        return session.query(RecordDTO.year).distinct()


