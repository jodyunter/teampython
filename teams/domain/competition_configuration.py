from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


# todo change configs to configurations
class CompetitionConfiguration(Base, YearRestricted):
    __tablename__ = "CompetitionConfigurations"

    oid = Column(String, primary_key=True)
    name = Column(String)
    order = Column(Integer)
    first_year = Column(Integer)
    last_year = Column(Integer)

    sub_competition_configurations = relationship("SubCompetitionConfiguration", back_populates="competition_configuration")
    team_configurations = relationship("CompetitionTeamConfiguration", back_populates="competition_configuration")

    def __init__(self, name, sub_competition_configurations, team_configurations, order, first_year, last_year, oid=None):
        self.name = name
        self.order = order
        self.sub_competition_configurations = sub_competition_configurations
        self.team_configurations = team_configurations
        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
            self.oid = oid

        YearRestricted.__init__(self, first_year, last_year)


