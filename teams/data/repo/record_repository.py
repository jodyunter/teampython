from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.base_repository import BaseRepository
from teams.data.repo.team_repository import TeamRepository


class RecordRepository(BaseRepository):
    team_repo = TeamRepository()

    def get_type(self):
        return RecordDTO

    def add(self, record_dto, session):
        session.add(record_dto)
        session.commit()

    def get_by_year(self, year, session):
        return session.query(self.get_type()).filter_by(year=year)
