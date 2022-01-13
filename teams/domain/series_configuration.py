# todo: mapping
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.utility.utility_classes import YearRestricted


class SeriesConfiguration(Base, YearRestricted):
    __tablename__ = "SeriesConfigurations"

    oid = Column(String, primary_key=True)
    name = Column(String)
    series_round = Column(Integer)
    series_rules_id = Column(String, ForeignKey("SeriesRules.oid"))
    series_rules = relationship("SeriesRules", foreign_keys=[series_rules_id])
    sub_competition_configuration_id = Column(String, ForeignKey('SubCompetitionConfigurations.oid'))
    sub_competition_configuration = relationship("SubCompetitionConfiguration",
                                                 foreign_keys=[sub_competition_configuration_id])
    home_team_group_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    home_team_group_configuration = relationship("CompetitionGroupConfiguration",
                                                 foreign_keys=[home_team_group_configuration_id])
    away_team_group_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    away_team_group_configuration = relationship("CompetitionGroupConfiguration",
                                                 foreign_keys=[away_team_group_configuration_id])
    home_team_value = Column(Integer)
    away_team_value = Column(Integer)
    winner_group_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    winner_group_configuration = relationship("CompetitionGroupConfiguration",
                                              foreign_keys=[winner_group_configuration_id])
    winner_rank_from_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    winner_rank_from_configuration = relationship("CompetitionGroupConfiguration",
                                                  foreign_keys=[winner_rank_from_configuration_id])
    loser_group_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    loser_group_configuration = relationship("CompetitionGroupConfiguration",
                                             foreign_keys=[loser_group_configuration_id])
    loser_rank_from_configuration_id = Column(String, ForeignKey('CompetitionGroupConfigurations.oid'))
    loser_rank_from_configuration = relationship("CompetitionGroupConfiguration",
                                                 foreign_keys=[winner_rank_from_configuration_id])
    first_year = Column(Integer)
    last_year = Column(Integer)

    def __init__(self, name, series_round, sub_competition_configuration,
                 home_team_group_configuration, home_team_value,
                 away_team_group_configuration, away_team_value,
                 series_rules,
                 winner_group_configuration, winner_rank_from_configuration,
                 loser_group_configuration, loser_rank_from_configuration,
                 first_year, last_year,
                 oid=None):
        self.series_round = series_round
        self.home_team_group_configuration = home_team_group_configuration
        self.home_team_value = home_team_value
        self.away_team_group_configuration = away_team_group_configuration
        self.away_team_value = away_team_value
        self.series_rules = series_rules
        self.winner_group_configuration = winner_group_configuration
        self.winner_rank_from_configuration = winner_rank_from_configuration
        self.loser_group_configuration = loser_group_configuration
        self.loser_rank_from_configuration = loser_rank_from_configuration

        self.name = name
        self.sub_competition_configuration = sub_competition_configuration
        self.oid = oid

        YearRestricted.__init__(self, first_year, last_year)
