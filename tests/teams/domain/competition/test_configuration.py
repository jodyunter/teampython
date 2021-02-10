#  create the competition
#  create the groups
#  create the teams
#  create the rankings
#  create the sub competions
#     create the series or records
#  create the games for the first sub competitions
#  schedule the games
#  everytime a playoff game is done, check if you need to schedule for for that series
#  everytime a playoff series is done, check if the round is done, if it's done, go to the next round
#  a playoff series sub competition can be done in order, and from groups create by previous rounds
#  so if you want a playoff round to run at the same time as a table, but the second round is after, it's another sub competition
#  all sub competitions must be done before we can go onto the next order of sub comps
#  all sub comps should be created at the same time but not setup until their order comes up so that we can rely on groups populated by previouis comps
import uuid

from teams.domain.competition import Competition, SubCompetition, CompetitionGroup, CompetitionTeam, CompetitionRanking
from teams.domain.competition_configuration import CompetitionConfiguration, CompetitionGroupConfiguration, \
    SubCompetitionConfiguration
from teams.domain.table_competition import TableRecord

comp_config = CompetitionConfiguration("My Comp", 1, 1, None, uuid.uuid4())


def create_competition_from_config(competition_config, year):
    return Competition(competition_config.name, year, False, False, False, False, uuid.uuid4())


#  assume a map of name:competition
def create_sub_competition_fromConfig(sub_competition_config, competitions):
    #  error if it doesn't exist because you did it out of order
    competition = competitions[sub_competition_config.competition_configuration.name]

    return SubCompetition(sub_competition_config.name, sub_competition_config.sub_competition_type,
                          competition, False, False, False, False, uuid.uuid4())


def create_competition_group_from_config(competition_group_config, sub_competitions, competition_groups):
    sub_competition = sub_competitions[competition_group_config.sub_competition_configuration.name]
    parent_group = None
    if competition_group_config.parent_group_configuratiom is not None:
        parent_group = competition_groups[competition_group_config.parent_group_configuratiom.name]

    return CompetitionGroup(competition_group_config.name,
                            parent_group, competition_group_config.group_type,
                            sub_competition, uuid.uuid4())


#  need to create rankings here
#  can be multiple competition team configurations, one for each group the team is in
#  we only need rankings if it is a ranking group
#  go up through the parent groups to add a ranking for each parent group
def process_competition_team_from_config(competition_team_config, competitions, competition_teams,
                                         competition_groups, competition_rankings, competition_records):
    competition = competitions[competition_team_config.competition_configuration.name]
    parent_team = competition_team_config.team
    competition_team = None
    if parent_team.name not in competition_teams:
        competition_team = CompetitionTeam(competition, parent_team, parent_team.name, parent_team.skill, uuid.uuid4())
        competition_teams[parent_team.name] = competition_team

    group = competition_groups[competition_team_config.group_configuration.name]
    if group.group_type == CompetitionGroupConfiguration.RANKING_TYPE:
        ranking_group = group
        while ranking_group is not None:
            if ranking_group.name not in competition_rankings:
                competition_rankings[group.name] = {}
            competition_rankings[group.name][competition_team.name] = CompetitionRanking(group, competition_team, -1, uuid.uuid4())

            ranking_group = ranking_group.parent_group

    #  create any records if needed
    if group.sub_competition.sub_competition_type == SubCompetitionConfiguration.TABLE_TYPE:
        if competition_team.name not in competition_records:
            competition_records[competition_team.name] = TableRecord(competition, -1, competition_team, competition.year, 0, 0, 0, 0, 0, competition_team.skill, uuid.uuid4())
