
# mapped
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain.team import Team


class CompetitionTeam(Team):
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("Competition", foreign_keys=[competition_id], back_populates="teams")
    parent_team_id = Column(String, ForeignKey('teams.oid'))
    parent_team = relationship("Team", remote_side=[Team.oid])

    __mapper_args__ = {
        'polymorphic_identity': 'competition_team'
    }

    def __init__(self, competition, parent_team, oid=None):
        self.competition = competition
        self.parent_team = parent_team

        Team.__init__(self, parent_team.name, parent_team.skill, True, oid)
