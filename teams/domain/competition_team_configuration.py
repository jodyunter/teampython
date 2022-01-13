from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.domain import Base, Team
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


class CompetitionTeamConfiguration(Base, YearRestricted):
    __tablename__ = "CompetitionTeamConfigurations"

    oid = Column(String, primary_key=True)
    first_year = Column(Integer)
    last_year = Column(Integer)
    competition_configuration_id = Column(String, ForeignKey('CompetitionConfigurations.oid'))
    competition_configuration = relationship("CompetitionConfiguration",
                                             foreign_keys=[competition_configuration_id],
                                             back_populates="team_configurations")
    group_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    group_configuration = relationship("CompetitionGroupConfiguration",
                                       foreign_keys=[group_configuration_id])
    team_id = Column(String, ForeignKey('teams.oid'))
    team = relationship("Team", remote_side=[Team.oid])

    def __init__(self, team, competition_configuration, group_configuration, first_year, last_year, oid=None):
        self.team = team
        self.competition_configuration = competition_configuration
        self.group_configuration = group_configuration
        self.oid = IDHelper.get_id(oid)

        YearRestricted.__init__(self, first_year, last_year)
