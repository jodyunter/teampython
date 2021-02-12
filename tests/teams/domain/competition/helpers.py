from teams.domain.competition import CompetitionTeam, TableRecord
from teams.domain.team import Team


def new_team(name, skill):
    return Team(name, skill, True)


def new_comp_team(competition, name, skill):
    team = new_team(name, skill)
    return CompetitionTeam(competition, team)


def new_comp_team_from_team(competition, team):
    return CompetitionTeam(competition, team)


def new_table_record(competition, name, skill):
    year = 1
    if competition is not None:
        year = competition.year

    return TableRecord(competition, -1,
                       new_comp_team_from_team(competition,
                                               new_team(name, skill)),
                       year, 0, 0, 0, 0, 0, skill)
