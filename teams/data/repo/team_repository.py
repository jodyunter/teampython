from teams.data.repo.repository import Repository
from teams.domain.competition_team import CompetitionTeam
from teams.domain.team import Team


class TeamRepository(Repository):

    def get_type(self):
        return Team

    def get_by_name(self, name, session):
        return session.query(self.get_type()).filter_by(name=name).first()

    def get_by_active_status(self, active, session):
        return session.query(self.get_type()).filter_by(active=active)


class CompetitionTeamRepository(TeamRepository):

    def get_type(self):
        return CompetitionTeam


