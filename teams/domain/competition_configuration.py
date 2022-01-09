from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from teams.domain import Base
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


# todo change configs to configurations
class CompetitionConfiguration(Base, YearRestricted):
    __tablename__ = "competitionconfigurations"

    oid = Column(String, primary_key=True)
    name = Column(String)
    order = Column(Integer)
    first_year = Column(Integer)
    last_year = Column(Integer)
    sub_competition_configs = relationship("SubCompetitionConfiguration", back_populates="competition_configuration")
    team_configs = relationship("CompetitionTeamConfiguration", back_populates="competition_configuration")

    def __init__(self, name, sub_competition_configs, team_configs, order, first_year, last_year, oid=None):
        self.name = name
        self.order = order
        self.sub_competitions = sub_competition_configs
        self.teams = team_configs
        self.oid = IDHelper.get_id(oid)

        YearRestricted.__init__(self, first_year, last_year)


# todo: mapping
class SeriesConfiguration(YearRestricted):

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


# todo: mapping
class TableGameConfiguration(YearRestricted):
    GROUP_TYPE = "Group"
    TEAM_TYPE = "Team"

    def __init__(self, name, sub_competition_configuration,
                 home_type, home_group, home_team,
                 away_type, away_group, away_team,
                 number_of_matches, home_and_away, first_year, last_year,
                 oid=None):
        self.home_type = home_type
        self.home_group = home_group
        self.home_team = home_team
        self.away_type = away_type
        self.away_group = away_group
        self.away_team = away_team
        self.number_of_matches = number_of_matches
        self.home_and_away = home_and_away

        self.name = name
        self.sub_competition_configuration = sub_competition_configuration
        self.oid = oid
        YearRestricted.__init__(first_year, last_year)

    @staticmethod
    def create_team_vs_group():
        pass

    @staticmethod
    def create_team_vs_team():
        pass

    @staticmethod
    def create_group_vs_group():
        pass

    @staticmethod
    def create_group_vs_self():
        pass
