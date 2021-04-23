from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.repository import Repository
from teams.data.repo.team_repository import TeamRepository


class RecordRepository(Repository):
    team_repo = TeamRepository()

    @staticmethod
    def get_by_year(year, session):
        return session.query(RecordDTO).filter_by(year=year)

    @staticmethod
    def get_by_team_and_year(team_id, year, session):
        return session.query(RecordDTO).filter_by(year=year, team_id=team_id).first()

    @staticmethod
    def get_by_team(team_id, session):
        return session.query(RecordDTO).filter_by(team_id=team_id)

    @staticmethod
    def get_by_rank(rank, session):
        return session.query(RecordDTO).filter_by(rank=rank)

    @staticmethod
    def get_list_of_seasons(session):
        return session.query(RecordDTO.year).distinct()


