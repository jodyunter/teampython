from sqlalchemy import String, Integer, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_competition import CompetitionDTO
from teams.domain.competition import CompetitionTeam
from teams.domain.team import Team


class TeamDTO(Base, Team):
    __tablename__ = "teams"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    skill = Column(Integer, default=5)
    active = Column(Boolean, default=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'team'
    }

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
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])
    parent_team_id = Column(String, ForeignKey('teams.oid'))
    parent_team = relationship("TeamDTO", foreign_keys=[parent_team_id])

    __mapper_args__ = {
        'polymorphic_identity': 'competition_team'
    }

    def __init__(self, competition_team):
        CompetitionTeam.__init__(self, competition_team.competition, competition_team.parent_team, competition_team.oid)
