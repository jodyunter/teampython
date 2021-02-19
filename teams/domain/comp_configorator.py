#  this class may become a service in the long run
from teams.domain.competition import CompetitionGroup, CompetitionTeam, Competition
from teams.domain.competition_configuration import CompetitionGameConfiguration, SubCompetitionConfiguration
from teams.domain.errors import DomainError
from teams.domain.series import SeriesByWins, SeriesByGoals
from teams.domain.series_rules import SeriesRules
from teams.domain.sub_competition import PlayoffSubCompetition


# TODO: Need to start using the setup flags

#  we need to create the competition, sub competitions,  competition teams, groups and series at the start
#  later on we need to be able to create and schedule games
class CompetitionConfigurator:

    @staticmethod
    def create_competition(competition_config, year):
        competition = Competition(competition_config.name, year, [], False, False, False, False)

        return competition

    @staticmethod
    def create_sub_competition(sub_competition_config, competition):
        if competition is None:
            raise DomainError("Can't setup sub competition if competition is not setup.")

        if sub_competition_config.name in [r.name for r in competition.sub_competitions]:
            raise DomainError(f"Sub competition {sub_competition_config.name} is already setup.")

        method_map = {
            SubCompetitionConfiguration.TABLE_TYPE: CompetitionConfigurator.create_table_sub_competition,
            SubCompetitionConfiguration.PLAYOFF_TYPE: CompetitionConfigurator.create_playoff_sub_competition
        }

        return method_map[sub_competition_config.sub_competition_type](sub_competition_config, competition)

    @staticmethod
    def create_competition_group(competition_group_config, current_groups, competition):
        if competition is None:
            raise DomainError("Competition has to exist before the groups can be setup.")

        current_group_list = [cg for cg in current_groups if cg.name == competition_group_config.name]
        if current_group_list is not None and len(current_group_list) == 1:
            return current_group_list[0]

        parent_group = None

        if competition_group_config.parent_group_configuration is not None:
            parent_group = [pg for pg in current_groups if
                            pg.name == competition_group_config.parent_group_configuration.name]
            if len(parent_group) == 0:
                # parent group is not setup
                parent_group = CompetitionConfigurator.create_competition_group(
                    competition_group_config.parent_group_configuration, current_groups, competition)
            else:
                parent_group = parent_group[0]

        sub_competition = None

        if competition_group_config.sub_competition_configuration is not None:
            sub_competition = [sb for sb in competition.sub_competitions if
                               sb.name == competition_group_config.sub_competition_configuration.name]
            if sub_competition is None or len(sub_competition) == 0:
                raise DomainError("You are setting up groups before sub competitions.")
            sub_competition = sub_competition[0]

        new_group = CompetitionGroup(competition_group_config.name,
                                     parent_group, sub_competition,
                                     [], competition_group_config.group_type)

        current_groups.append(new_group)

        return new_group

    @staticmethod
    def process_competition_team_configuration(team_configuration, current_groups, current_teams, competition):
        # check if competition exists
        if competition is None:
            raise DomainError("Competition has to exist before the teams and rankings can be setup.")

        if team_configuration is None:
            raise DomainError("No team configuration given.")

        #  check if group exists
        groups_with_name = [g for g in current_groups if g.name == team_configuration.group_configuration.name]
        if groups_with_name is None or len(groups_with_name) == 0:
            raise DomainError(f'Group {team_configuration.group_configuration.name} has not been created yet.')
        elif len(groups_with_name) > 1:
            raise DomainError(
                f'Group {team_configuration.group_configuration.name} has multiple groups {len(groups_with_name)}.')
        else:
            group = groups_with_name[0]

        # check if team exists
        team_created = [c for c in current_teams if c.parent_team.oid == team_configuration.team.oid]
        if team_created is None or len(team_created) == 0:
            team = CompetitionTeam(competition, team_configuration.team)
            current_teams.append(team)
        elif len(team_created) > 1:
            raise DomainError(f'Team {team_configuration.team.name} has too many {len(team_created)} teams created.')
        else:
            team = team_created[0]

        current_group = group
        while current_group is not None:
            current_group.add_team_to_group(team)
            current_group = current_group.parent_group

    @staticmethod
    def process_competition_game_configuration(competition_game_configuration, current_groups, sub_competition):
        if sub_competition is None:
            raise DomainError("Sub Competition must be created before competition games can be processed.")

        if sub_competition.competition is None:
            raise DomainError("Competition must be created before competition games can be processed.")

        method_map = {
            CompetitionGameConfiguration.TABLE_TYPE: CompetitionConfigurator.process_table_game_configuration,
            CompetitionGameConfiguration.PLAYOFF_TYPE: CompetitionConfigurator.process_series_game_configuration
        }

        method_map[competition_game_configuration.competition_game_type](competition_game_configuration, current_groups)

    #  this not used to schedule or create games
    #  this the pre-processing done before the competitions start
    #  right now table competitions don't do anything here as they only take teams from groups
    @staticmethod
    def process_series_game_configuration(series_game_configuration, current_groups, sub_competition):
        if sub_competition is None:
            raise DomainError("Sub Competition is null.")
        elif not isinstance(sub_competition, PlayoffSubCompetition):
            raise DomainError(f"Sub Competition {sub_competition.name} is not a playoff sub competition.")

        series_rules = series_game_configuration.series_rules

        if series_rules is None:
            raise DomainError(f"Series {series_game_configuration.name} does not have any rules.")

        required_groups = set()
        required_groups.add(series_game_configuration.home_team_group_configuration)
        required_groups.add(series_game_configuration.away_team_group_configuration)
        required_groups.add(series_game_configuration.winner_group_configuration)
        required_groups.add(series_game_configuration.loser_group_configuration)
        required_groups.add(series_game_configuration.winner_rank_from_configuration)
        required_groups.add(series_game_configuration.loser_rank_from_configuration)

        for gc in required_groups:
            CompetitionConfigurator.create_competition_group(gc, current_groups, sub_competition.competition)

        method_map = {
            SeriesRules.GOALS_TYPE: CompetitionConfigurator.process_series_by_goals_configuration,
            SeriesRules.WINS_TYPE: CompetitionConfigurator.processes_series_by_wins_configuration
        }

        new_series = method_map[series_game_configuration.series_rules.series_type](series_game_configuration, current_groups,
                                                                                    sub_competition)
        sub_competition.series.append(new_series)

    # TODO: we're assuming the group is there
    @staticmethod
    def get_group_from_list(group_name, group_list):
        found_list = [g for g in group_list if g.name == group_name]
        if found_list is None or len(found_list) == 0:
            raise DomainError(f"Group {group_name} was not found.  Need to create group before calling this.")
        elif len(found_list) > 1:
            raise DomainError(f"{group_name} has multiple {len(found_list)} entries.")
        else:
            return [g for g in group_list if g.name == group_name][0]

    @staticmethod
    def processes_series_by_wins_configuration(series_game_configuration, current_groups, sub_competition):
        series_rules = series_game_configuration.series_rules
        if series_rules.series_type != SeriesRules.WINS_TYPE:
            raise DomainError(f"Series {series_game_configuration.name} does not have the correct rules.")

        series = SeriesByWins(sub_competition, series_game_configuration.name, series_game_configuration.series_round,
                              None, None, 0, 0, series_rules,
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.home_team_group_configuration.name, current_groups),
                              series_game_configuration.home_team_value,
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.away_team_group_configuration.name, current_groups),
                              series_game_configuration.away_team_value,
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.winner_group_configuration.name, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.winner_rank_from_configuration.name, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.loser_group_configuration.name, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_game_configuration.loser_rank_from_configuration.name, current_groups),
                              False, False)

        return series

    @staticmethod
    def process_series_by_goals_configuration(series_game_configuration, current_groups, sub_competition):
        series_rules = series_game_configuration.series_rules
        if series_rules.series_type != SeriesRules.GOALS_TYPE:
            raise DomainError(f"Series {series_game_configuration.name} does not have the correct rules.")

        series = SeriesByGoals(sub_competition, series_game_configuration.name, series_game_configuration.series_round,
                               None, None, 0, 0, 0, series_rules,
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.home_team_group_configuration.name, current_groups),
                               series_game_configuration.home_team_value,
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.away_team_group_configuration.name, current_groups),
                               series_game_configuration.away_team_value,
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.winner_group_configuration.name, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.winner_rank_from_configuration.name, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.loser_group_configuration.name, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_game_configuration.loser_rank_from_configuration.name, current_groups),
                               False, False)

        return series

    @staticmethod
    def process_table_game_configuration(table_game_configuration, current_groups):
        #  this method isn't used at first
        pass
