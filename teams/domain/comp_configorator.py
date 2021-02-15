#  this class may become a service in the long run
from teams.domain.competition import CompetitionGroup, CompetitionTeam
from teams.domain.errors import DomainError


class CompetitionConfigurator:

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
            raise DomainError(f'Group {team_configuration.group_configuration.name} has multiple groups {len(groups_with_name)}.')
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

