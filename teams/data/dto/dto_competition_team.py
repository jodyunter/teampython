from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship

from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_team import TeamDTO
from teams.domain.competition import CompetitionTeam


class CompetitionTeamDTO(TeamDTO, CompetitionTeam):
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])
    parent_team_id = Column(String, ForeignKey('teams.oid'))
    parent_team = relationship("TeamDTO", remote_side=[TeamDTO.oid])

    __mapper_args__ = {
        'polymorphic_identity': 'competition_team'
    }

    def __init__(self, competition_team):
        competition = CompetitionDTO.get_dto(competition_team.competition)
        parent_dto = TeamDTO.get_dto(competition_team.parent_team)
        self.name = competition_team.name
        self.skill = competition_team.skill
        self.active = competition_team.active
        self.oid = competition_team.oid
        self.competition = competition
        self.parent_team = parent_dto
