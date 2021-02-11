import uuid

from teams.domain.competition import CompetitionTeam
from teams.domain.table_competition import TableRecord
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


def new_team(name, skill):
    return Team(name, skill, True, IDHelper.get_new_id())


def new_comp_team(competition, team):
    return CompetitionTeam(competition, team, IDHelper.get_new_id())


def new_table_record(competition, name, skill):
    year = 1
    if competition is not None:
        year = competition.year

    return TableRecord(competition, -1,
                       new_comp_team(competition,
                                     new_team(name, skill)),
                       year, 0, 0, 0, 0, 0, skill, IDHelper.get_new_id())