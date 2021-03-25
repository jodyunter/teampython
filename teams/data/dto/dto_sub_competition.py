from abc import ABC

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.competition import CompetitionGroup, RankingGroup
from teams.domain.sub_competition import SubCompetition, TableSubCompetition


class SubCompetitionDTO(ABC, Base, SubCompetition):
    __tablename__ = "subcompetitions"

    oid = Column(String, primary_key=True)
    sub_competition_type = Column(String)
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])
    order = Column(Integer)
    setup = Column(Boolean)
    started = Column(Boolean)
    finished = Column(Boolean)
    post_processed = Column(Boolean)

    def __init__(self, sub_competition):
        SubCompetition.__init__(self,
                                sub_competition.name,
                                sub_competition.sub_competition_type,
                                sub_competition.competition,
                                sub_competition.groups,
                                sub_competition.order,
                                sub_competition.setup,
                                sub_competition.started,
                                sub_competition.finished,
                                sub_competition.post_processed,
                                sub_competition.oid)

class TableSubCompetitionDTO(SubCompetitionDTO, TableSubCompetition)

class CompetitionGroupDTO(Base, CompetitionGroup):
    __tablename__ = "competitiongroup"

    oid = Column(String, primary_key=True)
    name = Column(String)
    parent_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    parent_group = relationship("CompetitionGroupDTO", foreign_keys=[parent_group_id])
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("SubCompetitionDTO", foreign_keys=[sub_competition_id])
    level = Column(Integer)
    group_type = Column(String)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'competition_group'
    }

    def __init__(self, competition_group):
        CompetitionGroup.__init__(self,
                                  competition_group.name,
                                  competition_group.parent_group,
                                  competition_group.sub_competition,
                                  competition_group.level,
                                  competition_group.rankings,
                                  competition_group.group_type,
                                  competition_group.oid)


class RankingGroupDTO(CompetitionGroupDTO, RankingGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'ranking_group'
    }

    def __init__(self, competition_group):
        RankingGroup.__init__(self,
                              competition_group.name,
                              competition_group.parent_group,
                              competition_group.sub_competition,
                              competition_group.level,
                              competition_group.rankings,
                              competition_group.oid)
