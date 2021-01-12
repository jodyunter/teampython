from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.base_repository import BaseRepository
from teams.data.repo.team_repository import TeamRepository


class RecordRepository(BaseRepository):
    team_repo = TeamRepository()

    def get_type(self):
        return RecordDTO

    def add(self, record, session):
        record_dto = RecordDTO.get_dto(record)
        session.add(record_dto)
        session.commit()

    def get_by_year(self, year, session):
        return session.query(self.get_type()).filter_by(year=year)

    def get_by_team_and_year(self, team_id, year, session):
        return session.query(self.get_type()).filter_by(year=year, team_id=team_id).first()

    def get_by_rank(self, rank, session):
        return session.query(self.get_type()).filter_by(rank=rank)

    def get_list_of_seasons(self, session):
        return session.query(self.get_type().year).group_by(RecordDTO.year)

