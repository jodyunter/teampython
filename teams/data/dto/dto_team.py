from sqlalchemy import String, Integer, Column, Boolean

from teams.data.dto.dto_base import Base
from teams.domain.competition import CompetitionTeam
from teams.domain.team import Team


class TeamDTO(Base, Team):
    __tablename__ = "teams"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    skill = Column(Integer, default=5)
    active = Column(Boolean, default=True)

    def __init__(self, team):
        Team.__init__(self, team.name, team.skill, team.active, team.oid)

    @staticmethod
    def get_dto(team):
        if not team.__class__ == TeamDTO:
            team_dto = TeamDTO(team)
        else:
            team_dto = team

        return team_dto


class CompetitionTeamDTO(TeamDTO, CompetitionTeam):

    def __init__(self, competition_team):

        CompetitionTeam.__init__(self, competition_team.competition, competition_team.parent_team, competition_team.oid)
