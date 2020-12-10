from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.base_repository import BaseRepository


class TeamRepository(BaseRepository):
    def get_type(self):
        return TeamDTO

    def get_by_name(self, name, session):
        return session.query(self.get_type()).filter_by(name=name).first()

    def add(self, team_dto, session):
        session.add(team_dto)

