from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.base_repository import BaseRepository


class TeamRepository(BaseRepository):
    def get_type(self):
        return TeamDTO

    def get_by_name(self, name, session):
        return session.query(self.get_type()).filter_by(name=name).first()

    def get_by_active_status(self, active, session):
        return session.query(self.get_type()).filter_by(active=active)


