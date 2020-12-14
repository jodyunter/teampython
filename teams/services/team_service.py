from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.team_repository import TeamRepository
from teams.domain.team import Team
from teams.services.base_service import BaseService
from teams.services.view_models.team_view_models import TeamViewModel


class TeamService(BaseService):
    repo = TeamRepository()

    def create(self, name, skill, session=None):
        commit = session is None
        session = self.get_session(session)

        dto = Team(name, skill, self.get_new_id())
        self.repo.add(dto, session)

        self.commit(session, commit)

    def update(self, oid, name, skill, session=None):
        commit = session is None
        session = self.get_session(session)

        team = self.repo.get_by_oid(oid, session)
        team.name = name
        team.skill = skill

        self.commit(session, commit)

    def get_all(self, session=None):
        session = self.get_session(session)

        team_list = self.repo.get_all(session)
        return [TeamViewModel(t.oid, t.name, t.skill) for t in team_list]

    def get_team_by_name(self, name, session=None):
        session = self.get_session(session)
        team = self.repo.get_by_name(name, session)
        return TeamViewModel(team.oid, team.name, team.skill)

    def get_by_id(self, oid, session=None):
        session = self.get_session(session)
        team = self.repo.get_by_oid(oid, session)
        return TeamViewModel(team.oid, team.name, team.skill)
