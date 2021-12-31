from teams.domain.competition import Competition
from teams.domain.competition_team import CompetitionTeam
from teams.domain.table_record import TableRecord
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


def create_default_competition_for_testing(name, year=1, sub_comp=None, teams=None):
    if sub_comp is None:
        sub_comp = []

    if teams is None:
        teams = []

    new_comp = Competition(name, year, sub_comp, teams, 1, False, False, False, False)
    return new_comp
