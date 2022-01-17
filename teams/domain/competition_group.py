# mapped
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.domain.base import Base
from teams.domain.competition_group_configuration import CompetitionGroupConfiguration
from teams.domain.competition_ranking import CompetitionRanking
from teams.domain.utility.utility_classes import IDHelper


class CompetitionGroup(Base):
    __tablename__ = "competitiongroups"

    oid = Column(String, primary_key=True)
    name = Column(String)
    parent_group_id = Column(String, ForeignKey('competitiongroups.oid'))
    parent_group = relationship("CompetitionGroup", remote_side=[oid])
    sub_competition_id = Column(String, ForeignKey('SubCompetitions.oid'))
    sub_competition = relationship("SubCompetition", foreign_keys=[sub_competition_id], back_populates="groups")
    rankings = relationship("CompetitionRanking", back_populates="group")
    level = Column(Integer)
    group_type = Column(String)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'competition_group'
    }

    def __init__(self, name, parent_group, sub_competition, level, rankings, group_type, oid=None):
        self.name = name
        self.parent_group = parent_group
        self.sub_competition = sub_competition
        self.group_type = group_type
        self.level = level
        if rankings is None:
            self.rankings = []
        else:
            self.rankings = rankings
        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
            self.oid = oid

    def add_team_to_group(self, competition_team, rank=None):
        if rank is None:
            rank = -1
        team_in_group = [t for t in self.rankings if t.team.oid == competition_team.oid]
        if team_in_group is None or len(team_in_group) == 0:
            CompetitionRanking(self, competition_team, rank)
            # self.rankings.append(CompetitionRanking(self, competition_team, rank))
        else:
            return

    def get_rank_for_team(self, team):
        return [r.rank for r in self.rankings if r.team.oid == team.oid][0]

    def get_team_by_rank(self, rank):
        return [t for t in self.rankings if t.rank == rank][0].team

    def get_ranking_for_team(self, team):
        return [r for r in self.rankings if r.team.oid == team.oid][0]

    # assume 1 is the first
    def get_team_by_order(self, order, reverse=False):
        self.rankings.sort(key=lambda team_rank: team_rank.rank)

        return self.rankings[order - 1]

    def set_rank(self, team, rank):
        self.get_ranking_for_team(team).rank = rank


# mapped
class RankingGroup(CompetitionGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'ranking_group'
    }

    def __init__(self, name, parent_group, sub_competition, level, rankings, oid=None):
        CompetitionGroup.__init__(self, name, parent_group, sub_competition, level, rankings,
                                  CompetitionGroupConfiguration.RANKING_TYPE, oid)

