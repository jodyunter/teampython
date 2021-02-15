#  this class may become a service in the long run
from teams.domain.competition import CompetitionGroup
from teams.domain.errors import DomainError


class CompetitionConfigurator:

    @staticmethod
    def create_competition_group(competition_group_config, current_groups, competition):
        if competition is None:
            raise DomainError("Competition has to exist before the groups can be setup.")

        if len([cg for cg in current_groups if cg.name == competition_group_config.name]) != 0:
            return  # group is already setup. this might happen below

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
