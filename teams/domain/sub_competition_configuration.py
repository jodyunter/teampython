from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


#todo work on changing config and configs to configuration and configurations
class SubCompetitionConfiguration(Base, YearRestricted):
    PLAYOFF_TYPE = "Playoff"
    TABLE_TYPE = "Table"

    __tablename__ = "subcompetitionconfigurations"

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'sub_competition_configuration'
    }

    oid = Column(String, primary_key=True)
    name = Column(String)
    sub_competition_type = Column(String)
    competition_configuration_id = Column(String, ForeignKey('competition_configurations.oid'))
    competition_configuration = relationship("CompetitionConfiguration", foreign_keys=[competition_configuration_id],
                                             back_populates="sub_competition_configurations")
    competition_group_configs = relationship("CompetitionGroupConfiguration",
                                             back_populates="sub_competition_configuration")
    competition_team_configs = relationship("CompetitionTeamConfiguration",
                                            back_populates="sub_competition_configuration")
    order = Column(Integer)
    first_year = Column(Integer)
    last_year = Column(Integer)

    def __init__(self, name, competition_configuration, competition_group_configs, competition_team_configs, order,
                 sub_competition_type, first_year, last_year, oid=None):
        self.name = name
        self.competition_configuration = competition_configuration

        if competition_group_configs is None:
            self.competition_group_configs = []
        else:
            self.competition_groups = competition_group_configs

        self.order = order
        self.sub_competition_type = sub_competition_type

        if competition_team_configs is None:
            self.competition_teams = competition_team_configs
        else:
            self.competition_teams = []

        self.oid = IDHelper.get_id(oid)

        YearRestricted.__init__(self, first_year, last_year)
