from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.repository import Repository


class TeamRepository(Repository):


    @staticmethod
    def get_by_name(name, session):
        return session.query(TeamDTO).filter_by(name=name).first()

    @staticmethod
    def get_by_active_status(active, session):
        return session.query(TeamDTO).filter_by(active=active)


