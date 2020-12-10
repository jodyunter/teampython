from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.team_repository import TeamRepository
from teams.services.base_service import BaseService
from teams.services.view_models.team_views import TeamView


class TeamService(BaseService):
    repo = TeamRepository()

    def create(self, name, skill):
        session = self.repo.get_session()
        dto = TeamDTO(name, skill, self.get_new_id())
        self.repo.add(dto, session)
        session.commit()

    def update(self, oid, name, skill):
        session = self.repo.get_session()
        team = self.repo.get_by_oid(oid, session)
        team.name = name
        team.skill = skill
        session.commit()

    def get_all(self):
        session = self.repo.get_session()
        team_list = self.repo.get_all(session)
        return [TeamView(t.oid, t.name, t.skill) for t in team_list]

    def get_team_by_name(self, name):
        session = self.repo.get_session()
        team = self.repo.get_by_name(name, session)
        return TeamView(team.oid, team.name, team.skill)

    def get_by_id(self, oid):
        session = self.repo.get_session()
        team = self.repo.get_by_oid(oid, session)
        return TeamView(team.oid, team.name, team.skill)
