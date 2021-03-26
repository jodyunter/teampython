from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship

from teams.data.dto.dto_team import TeamDTO
from teams.domain.competition import CompetitionTeam


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
