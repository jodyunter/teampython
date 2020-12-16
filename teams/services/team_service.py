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
        maximum = 20
        minimum = 0
        max_score = 200
        commit = session is None
        session = self.get_session(session)

        teams = self.repo.get_all(session)

        skill_change = {
            "0": [0, 60],
            "1": [40, 60],
            "2": [40, 60],
            "3": [40, 60],
            "4": [40, 60],
            "5": [40, 100],
            "6": [80, 100],
            "7": [80, 100],
            "8": [80, 100],
            "9": [80, 100],
            "10": [100, 140],
            "11": [100, 140],
            "12": [100, 140],
            "13": [100, 140],
            "14": [100, 140],
            "15": [100, 140],
            "16": [140, 180],
            "17": [140, 180],
            "18": [140, 180],
            "19": [140, 180],
            "20": [140, 200]
        }

        for t in teams:
            old_skill = t.skill
            score = random.randint(0, max_score)
            # normalize in case there was a change in process or data
            if t.skill > maximum:
                t.skill = maximum

            if t.skill < minimum:
                t.skill = minimum

            down = skill_change[str(t.skill)][0]
            up = skill_change[str(t.skill)][1]

            if score < down:
                t.skill -= 1

            if score > up:
                t.skill += 1

            if t.skill > maximum:
                t.skill = maximum

            if t.skill < minimum:
                t.skill = minimum

            print(t.name + " Old: " + str(old_skill) + " New:" + str(t.skill) +
                  " score: " + str(score) +
                  " up: " + str(up) + " down: " + str(down))

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
