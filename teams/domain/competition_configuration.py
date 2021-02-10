from teams.domain.utility.utility_classes import YearRestricted


class CompetitionConfiguration(YearRestricted):

    def __init__(self, name, order,  first_year, last_year, oid):
        self.name = name
        self.order = order
        self.oid = oid

        YearRestricted.__init__(first_year, last_year)


class SubCompetition(YearRestricted):

    def __init__(self, name, competition_configuration, order, type, first_year, last_year, oid):
        self.name = name
        self.competition_configuration = competition_configuration
        self.order = order
        self.type = type
        self.oid = oid

        YearRestricted.__init__(first_year, last_year)


class CompetitionGroupConfiguration(YearRestricted):

    def __init__(self, name, sub_competition_configuration, parent_group_configuration, group_level, first_year,
                 last_year, oid):
        self.name = name
        self.sub_competition_configuration = sub_competition_configuration
        self.parent_group_configuration = parent_group_configuration
        self.group_level = group_level
        self.oid = oid

        YearRestricted.__init__(first_year, last_year)


class CompetitionTeamConfiguration(YearRestricted):
    REGIONAL_TYPE = "Regional"
    RANKING_TYPE = "Ranking"

    def __init__(self, team, competition_configuration, group_configuration, group_type, first_year, last_year, oid):
        self.team = team
        self.competition_configuration = competition_configuration
        self.group_configuration = group_configuration
        self.group_type = group_type
        self.oid = oid

        YearRestricted.__init__(first_year, last_year)


class CompetitionGameConfiguration(YearRestricted):
    TABLE_TYPE = "Table"
    PLAYOFF_TYPE = "Playoff"

    def __init__(self, name, sub_competition_configuration, competition_game_type, first_year, last_year, oid):
        self.name = name
        self.sub_competition_configuration = sub_competition_configuration
        self.competition_game_type = competition_game_type
        self.oid = oid

        YearRestricted.__init__(first_year, last_year)


class SeriesConfiguration(CompetitionGameConfiguration):

    def __init__(self, name, series_round, sub_competition_configuration,
                 home_team_group_configuration, home_team_value,
                 away_team_group_configuration, away_team_value,
                 series_rules, game_rules,
                 winner_group_configuration, loser_group_configuration,
                 first_year, last_year,
                 oid):
        self.series_round = series_round
        self.home_team_group_configuration = home_team_group_configuration
        self.home_team_value = home_team_value
        self.away_team_group_configuration = away_team_group_configuration
        self.away_team_value = away_team_value
        self.series_rules = series_rules
        self.game_rules = game_rules
        self.winner_group_configuration = winner_group_configuration
        self.loser_group_configuration = loser_group_configuration

        CompetitionGameConfiguration.__init__(name, sub_competition_configuration,
                                              CompetitionGameConfiguration.PLAYOFF_TYPE,
                                              first_year, last_year, oid)


class TableGameConfiguration(CompetitionGameConfiguration):
    GROUP_TYPE = "Group"
    TEAM_TYPE = "Team"

    def __init__(self, name, sub_competition_configuration,
                 home_type, home_group, home_team,
                 away_type, away_group, away_team,
                 number_of_matches, home_and_away, first_year, last_year,
                 oid):
        self.home_type = home_type
        self.home_group = home_group
        self.home_team = home_team
        self.away_type = away_type
        self.away_group = away_group
        self.away_team = away_team
        self.number_of_matches = number_of_matches
        self.home_and_away = home_and_away

        CompetitionGameConfiguration.__init__(name, sub_competition_configuration,
                                              CompetitionGameConfiguration.TABLE_TYPE,
                                              first_year, last_year, oid)