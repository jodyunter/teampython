
# mapped
from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.domain.base import Base
from teams.domain.utility.utility_classes import IDHelper


class CompetitionRanking(Base):
    __tablename__ = "competitionranking"
    oid = Column(String, primary_key=True)
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("Competition", foreign_keys=[competition_id])
    team_id = Column(String, ForeignKey('teams.oid'))
    team = relationship("Team", foreign_keys=[team_id])
    group_id = Column(String, ForeignKey('competitiongroups.oid'))
    group = relationship("CompetitionGroup", foreign_keys=[group_id], back_populates="rankings")
    rank = Column(Integer)

    def __init__(self, competition_group, competition_team, rank, oid=None):
        self.group = competition_group
        self.team = competition_team
        self.rank = rank
        self.oid = IDHelper.get_id(oid)

    @staticmethod
    def get_dictionary_of_groups_from_rankings(competition_rankings):
        ranking_group_dict = {}

        for tr in competition_rankings:
            if tr.group.name not in ranking_group_dict:
                ranking_group_dict[tr.group.name] = []

            ranking_group_dict[tr.group.name].append(tr)

        return ranking_group_dict
