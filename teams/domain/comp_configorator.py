#  this class may become a service in the long run
from teams.domain.competition import CompetitionGroup, CompetitionTeam, Competition, TableRecord
from teams.domain.competition_configuration import SubCompetitionConfiguration
from teams.domain.errors import DomainError
from teams.domain.series import SeriesByWins, SeriesByGoals
from teams.domain.series_rules import SeriesRules
from teams.domain.sub_competition import PlayoffSubCompetition, TableSubCompetition


# TODO: Need to start using the setup flags

#  we need to create the competition, sub competitions,  competition teams, groups and series at the start
#  later on we need to be able to create and schedule games
class CompetitionConfigurator:

    @staticmethod
    def create_competition(competition_config, year):
        competition = Competition(competition_config.name, year, [], [], False, False, False, False)

        competition_config.sub_competitions.sort(key=lambda sc: sc.order)

        for sub in competition_config.sub_competitions:
            CompetitionConfigurator.create_sub_competition(sub, competition)

        # create teams
        for team_config in competition_config.teams:
            CompetitionConfigurator.process_competition_team_configuration(team_config, competition)

        # setup initial games

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

        sub_comp = method_map[sub_competition_config.sub_competition_type](sub_competition_config, competition)

        return sub_comp

    @staticmethod
    def create_playoff_sub_competition(sub_competition_config, competition):
        sub_comp = PlayoffSubCompetition(sub_competition_config.name,
                                         [],
                                         competition, [],
                                         sub_competition_config.order,
                                         1,
                                         False, False, False, False)

        competition.sub_competitions.append(sub_comp)

        CompetitionConfigurator.create_sub_competition_groups(sub_competition_config, competition)

        for s in sub_competition_config.series:
            CompetitionConfigurator.process_series_configuration(s, sub_comp)

        return sub_comp

    @staticmethod
    def create_table_sub_competition(sub_competition_config, competition):
        sub_comp = TableSubCompetition(sub_competition_config.name,
                                       [],
                                       competition,
                                       [],
                                       sub_competition_config.order,
                                       False, False, False, False)

        competition.sub_competitions.append(sub_comp)

        CompetitionConfigurator.create_sub_competition_groups(sub_competition_config, competition)

        return sub_comp

    @staticmethod
    def create_sub_competition_groups(sub_comp_config, competition):
        for g in sub_comp_config.competition_groups:
            CompetitionConfigurator.create_competition_group(g, competition)

    @staticmethod
    def create_competition_group(competition_group_config, competition):
        if competition_group_config is not None:
            if competition is None:
                raise DomainError("Competition has to exist before the groups can be setup.")

            current_groups = competition.get_all_groups()

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
                        competition_group_config.parent_group_configuration, competition)
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

            sub_competition.groups.append(new_group)

            return new_group

    @staticmethod
    def process_competition_team_configuration(team_configuration, competition):
        # check if competition exists
        if competition is None:
            raise DomainError("Competition has to exist before the teams and rankings can be setup.")

        if team_configuration is None:
            raise DomainError("No team configuration given.")

        current_groups = competition.get_all_groups()

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
        team_created = [c for c in competition.teams if c.parent_team.oid == team_configuration.team.oid]
        if team_created is None or len(team_created) == 0:
            team = CompetitionTeam(competition, team_configuration.team)
            if team_configuration.group_configuration.sub_competition_configuration.sub_competition_type == SubCompetitionConfiguration.TABLE_TYPE:
                table_comp = [sc for sc in competition.sub_competitions if sc.name == team_configuration.group_configuration.sub_competition_configuration.name][0]
                table_comp.records.append(
                    TableRecord(table_comp, -1, team, competition.year, 0, 0, 0, 0, 0, team.skill)
                )
            competition.teams.append(team)
        elif len(team_created) > 1:
            raise DomainError(f'Team {team_configuration.team.name} has too many {len(team_created)} teams created.')
        else:
            team = team_created[0]

        current_group = group
        while current_group is not None:
            current_group.add_team_to_group(team)
            current_group = current_group.parent_group

    #  this not used to schedule or create games
    #  this the pre-processing done before the competitions start
    #  right now table competitions don't do anything here as they only take teams from groups
    # todo: test the errors raised
    @staticmethod
    def process_series_configuration(series_configuration, sub_competition):
        if sub_competition is None:
            raise DomainError("Sub Competition must be created before competition games can be processed.")

        if sub_competition.competition is None:
            raise DomainError("Competition must be created before competition games can be processed.")

        if not isinstance(sub_competition, PlayoffSubCompetition):
            raise DomainError(f"Sub Competition {sub_competition.name} is not a playoff sub competition.")

        series_rules = series_configuration.series_rules

        if series_rules is None:
            raise DomainError(f"Series {series_configuration.name} does not have any rules.")

        required_groups = set()
        required_groups.add(series_configuration.home_team_group_configuration)
        required_groups.add(series_configuration.away_team_group_configuration)
        required_groups.add(series_configuration.winner_group_configuration)
        required_groups.add(series_configuration.loser_group_configuration)
        required_groups.add(series_configuration.winner_rank_from_configuration)
        required_groups.add(series_configuration.loser_rank_from_configuration)

        for gc in required_groups:
            CompetitionConfigurator.create_competition_group(gc, sub_competition.competition)

        method_map = {
            SeriesRules.GOALS_TYPE: CompetitionConfigurator.process_series_by_goals_configuration,
            SeriesRules.WINS_TYPE: CompetitionConfigurator.processes_series_by_wins_configuration
        }

        new_series = method_map[series_configuration.series_rules.series_type](series_configuration, sub_competition)
        sub_competition.series.append(new_series)
        new_series.sub_competition = sub_competition

    @staticmethod
    def get_group_from_list(group_config, group_list):
        if group_config is not None:
            found_list = [g for g in group_list if g.name == group_config.name]
            if found_list is None or len(found_list) == 0:
                raise DomainError(f"Group {group_config.name} was not found.  Need to create group before calling this.")
            elif len(found_list) > 1:
                raise DomainError(f"{group_config.name} has multiple {len(found_list)} entries.")
            else:
                return [g for g in group_list if g.name == group_config.name][0]
        else:
            return None

    @staticmethod
    def processes_series_by_wins_configuration(series_configuration, sub_competition):
        series_rules = series_configuration.series_rules
        if series_rules.series_type != SeriesRules.WINS_TYPE:
            raise DomainError(f"Series {series_configuration.name} does not have the correct rules.")

        current_groups = sub_competition.competition.get_all_groups()

        series = SeriesByWins(sub_competition, series_configuration.name, series_configuration.series_round,
                              None, None, 0, 0, series_rules,
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.home_team_group_configuration, current_groups),
                              series_configuration.home_team_value,
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.away_team_group_configuration, current_groups),
                              series_configuration.away_team_value,
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.winner_group_configuration, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.winner_rank_from_configuration, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.loser_group_configuration, current_groups),
                              CompetitionConfigurator.get_group_from_list(
                                  series_configuration.loser_rank_from_configuration, current_groups),
                              False, False)

        return series

    @staticmethod
    def process_series_by_goals_configuration(series_configuration, current_groups, sub_competition):
        series_rules = series_configuration.series_rules
        if series_rules.series_type != SeriesRules.GOALS_TYPE:
            raise DomainError(f"Series {series_configuration.name} does not have the correct rules.")

        series = SeriesByGoals(sub_competition, series_configuration.name, series_configuration.series_round,
                               None, None, 0, 0, 0, series_rules,
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.home_team_group_configuration, current_groups),
                               series_configuration.home_team_value,
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.away_team_group_configuration, current_groups),
                               series_configuration.away_team_value,
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.winner_group_configuration, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.winner_rank_from_configuration, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.loser_group_configuration, current_groups),
                               CompetitionConfigurator.get_group_from_list(
                                   series_configuration.loser_rank_from_configuration, current_groups),
                               False, False)

        return series

    @staticmethod
    def process_table_game_configuration(table_game_configuration, current_groups):
        #  this method isn't used at first
        pass
