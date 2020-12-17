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
        maximum = 25
        minimum = 0
        max_score = 400
        sub_value = 200
        commit = session is None
        session = self.get_session(session)

        teams = self.repo.get_all(session)

        skill_change = {
            "0": [100, 0],
            "1": [90, -10],
            "2": [80, -20],
            "3": [70, -30],
            "4": [60, -40],
            "5": [50, -50],
            "6": [40, -60],
            "7": [30, -70],
            "8": [20, -80],
            "9": [10, -90],
            "10": [0, -100]
        }

        for t in teams:
            old_skill = t.skill
            score = random.randint(0, max_score) - sub_value
            # normalize in case there was a change in process or data
            if t.skill > maximum:
                t.skill = maximum

            if t.skill < minimum:
                t.skill = minimum

            down = skill_change[str(t.skill)][1]
            up = skill_change[str(t.skill)][0]

            if score > 0:
                if score < up:
                    t.skill += 1

            if score < 0:
                if score > down:
                    t.skill -= 1

            if t.skill > maximum:
                t.skill = maximum

            if t.skill < minimum:
                t.skill = minimum

            # print(t.name + " Old: " + str(old_skill) + " New:" + str(t.skill) +
            #       " score: " + str(score) +
            #       " up: " + str(up) + " down: " + str(down))

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
