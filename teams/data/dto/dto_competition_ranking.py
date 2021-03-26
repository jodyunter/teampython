from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.competition import CompetitionRanking


# todo: create repo
class CompetitionRankingDTO(Base, CompetitionRanking):
    __tablename__ = "competitionranking"
    oid = Column(String, primary_key=True)
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])
    parent_team_id = Column(String, ForeignKey('teams.oid'))
    parent_team = relationship("TeamDTO", foreign_keys=[parent_team_id])
    rank = Column(Integer)

    def __init__(self, competition_ranking):
        CompetitionRanking.__init__(self,
                                    competition_ranking.competition_group,
                                    competition_ranking.competition_team,
                                    competition_ranking.rank,
                                    competition_ranking.oid)