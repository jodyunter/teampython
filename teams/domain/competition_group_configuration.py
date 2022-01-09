# todo: do we need regional groups if they are just the same thing?
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.errors import DomainError
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


# todo rename all tables to camel case
class CompetitionGroupConfiguration(Base, YearRestricted):
    REGIONAL_TYPE = "Regional"
    RANKING_TYPE = "Ranking"

    __tablename__ = "CompetitionGroupConfigurations"

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'competition_group_configuration'
    }

    oid = Column(String, primary_key=True)
    name = Column(String)
    parent_group_configuration_id = Column(String, ForeignKey('competitiongroupconfigurations.oid'))
    parent_group_configuration = relationship("CompetitionGroupConfiguration", remote_side=[oid])
    sub_competition_configuration_id = Column(String, ForeignKey('subcompetitionconfigurations.oid'))
    sub_competition_configuration = relationship("SubCompetitionConfiguration",
                                                 foreign_keys=[sub_competition_configuration_id],
                                                 back_populates="competition_group_configs")
    group_level = Column(Integer)
    group_type = Column(String)
    first_year = Column(Integer)
    last_year = Column(Integer)

    def __init__(self, name, sub_competition_configuration, parent_group_configuration, group_level, group_type,
                 first_year, last_year, oid=None):
        self.name = name
        if sub_competition_configuration is None:
            raise DomainError("CompetitionGroupConfiguration must be part of a sub competition.")
        self.sub_competition_configuration = sub_competition_configuration
        self.parent_group_configuration = parent_group_configuration
        self.group_level = group_level
        self.group_type = group_type
        self.oid = IDHelper.get_id(oid)

        YearRestricted.__init__(self, first_year, last_year)


class RankingGroupConfiguration(CompetitionGroupConfiguration):
    __mapper_args__ = {
        'polymorphic_identity': 'ranking_group_configuration'
    }

    def __init__(self, name, sub_competition_configuration, parent_group_configuration, group_level,
                 first_year, last_year, oid=None):
        CompetitionGroupConfiguration.__init__(self, name, sub_competition_configuration, parent_group_configuration,
                                               group_level,
                                               CompetitionGroupConfiguration.RANKING_TYPE, first_year, last_year, oid)
