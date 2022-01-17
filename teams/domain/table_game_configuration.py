# todo this is for future schedule rules
from teams.domain.utility.utility_classes import YearRestricted, IDHelper


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
        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
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
