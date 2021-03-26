from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.competition import CompetitionGroup


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

