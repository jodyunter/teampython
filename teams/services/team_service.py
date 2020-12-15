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

    def update_skills(self, random, session=None):
        commit = session is None
        session = self.get_session(session)

        teams = self.repo.get_all(session)

        for t in teams:
            to_go_up = 100 - int((100 - 5 * t.skill) / 2)
            to_go_down = 100 - int((5 * t.skill) / 2)

            up_score = random.randint(0, 100)
            down_score = random.randint(0, 100)

            if up_score > to_go_up:
                t.skill += 1

            if down_score > to_go_down:
                t.skill -= 1

            if t.skill > 20:
                t.skill = 20

            if t.skill < 0:
                t.skill = 0

        self.commit(session, commit)

    def get_all(self, session=None):
        session = self.get_session(session)

        team_list = self.repo.get_all(session)
        return [TeamViewModel(t.oid, t.name, t.skill) for t in team_list]

    def get_team_by_name(self, name, session=None):
        session = self.get_session(session)
        team = self.repo.get_by_name(name, session)
        if team is None:
            return None
        else:
            return TeamViewModel(team.oid, team.name, team.skill)

    def get_by_id(self, oid, session=None):
        session = self.get_session(session)
        team = self.repo.get_by_oid(oid, session)
        if team is None:
            return None
        else:
            return TeamViewModel(team.oid, team.name, team.skill)
