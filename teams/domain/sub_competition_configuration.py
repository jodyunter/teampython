from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


# todo work on changing config and configs to configuration and configurations
class SubCompetitionConfiguration(Base, YearRestricted):
    PLAYOFF_TYPE = "Playoff"
    TABLE_TYPE = "Table"

    __tablename__ = "SubCompetitionConfigurations"

    oid = Column(String, primary_key=True)
    name = Column(String)
    sub_competition_type = Column(String)
    competition_configuration_id = Column(String, ForeignKey('CompetitionConfigurations.oid'))
    competition_configuration = relationship("CompetitionConfiguration", foreign_keys=[competition_configuration_id],
                                             back_populates="sub_competition_configurations")
    competition_group_configs = relationship("CompetitionGroupConfiguration",
                                             back_populates="sub_competition_configuration")
    order = Column(Integer)
    first_year = Column(Integer)
    last_year = Column(Integer)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'sub_competition_configuration'
    }

    def __init__(self, name, competition_configuration, competition_group_configs, order,
                 sub_competition_type, first_year, last_year, oid=None):
        self.name = name
        self.competition_configuration = competition_configuration

        if competition_group_configs is None:
            self.competition_group_configs = []
        else:
            self.competition_group_configs = competition_group_configs

        self.order = order
        self.sub_competition_type = sub_competition_type

        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
            self.oid = oid

        YearRestricted.__init__(self, first_year, last_year)
