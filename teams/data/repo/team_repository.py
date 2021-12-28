from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.repository import Repository


class TeamRepository(Repository):


    def get_by_name(self, name, session):
        return session.query(TeamDTO).filter_by(name=name).first()

    def get_by_active_status(self, active, session):
        return session.query(TeamDTO).filter_by(active=active)


