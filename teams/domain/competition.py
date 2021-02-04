from abc import ABC, abstractmethod


class Competition(ABC):

    def __init__(self, year, name, setup, started, complete):
        self.year = year
        self.name = name
        self.setup = setup
        self.started = started
        self.complete = complete

    @abstractmethod
    def setup(self, rules, **kwargs):
        pass


class TableCompetition:

    def __init__(self, year, name, teams, divisions, rankings, setup, started, complete):
        pass



class TableDivision:

    def __init__(self, table_competition, name, division_level, division_rank):
        self.table_competition = table_competition
        self.name = name
        self.division_level
        self.division_rank


class TableTeamRanking:

    def __init__(self, table_team, table_division, rank):
        self.rank = rank
        self.table_team = table_team
        self.table_division = table_division



class TableTeam:
    pass


class TableCompetitionTeamRule:

    def __init__(self, team, division_name):
        self.team = team
        self.division_name = division_name


class TableCompetitionScheduleRule:
    pass
