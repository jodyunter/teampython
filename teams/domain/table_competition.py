from teams.domain.game import Game
from teams.domain.record import Record
from teams.domain.utility.utility_classes import YearRestricted


class TableCompetition:

    def __init__(self, year, name, teams, records, divisions, rankings, setup, started, complete):
        self.name = name
        self.teams = teams
        self.records = records
        self.divisions = divisions
        self.rankings = rankings
        self.year = year
        self.setup = setup
        self.started = started
        self.complete = complete

    @staticmethod
    def sort_records(team_records):
        team_records.sort(key=lambda rec: (-rec.points, rec.games, -rec.wins, -rec.goal_difference))

    @staticmethod
    def sort_records_by_division(table_rankings):
        table_rankings.sort(key=lambda tr: (-tr.record.points, tr.record.games, -tr.record.wins,
                                            tr.record.games, -tr.record.goal_difference))
        count = 1
        for t in table_rankings:
            t.rank = count
            count += 1


class TableDivision:

    def __init__(self, competition, name, parent_division, division_level, division_rank):
        self.competition = competition
        self.name = name
        self.division_level = division_level
        self.division_rank = division_rank
        self.parent_division = parent_division


class TableRanking:

    def __init__(self, table_record, table_division, rank):
        self.rank = rank
        self.record = table_record
        self.division = table_division


class TableRecord(Record):

    def __init__(self, competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid):
        self.competition = competition
        self.oid = oid
        self.rank = rank
        self.team = team
        self.year = year
        self.wins = wins
        self.loses = loses
        self.ties = ties
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.skill = skill


class TableGame(Game):

    def __init__(self, competition, year, day, home_team, away_team, home_score, away_score, complete, processed, rules, oid):
        self.competition = competition
        super().__init__(year, day, home_team, away_team, home_score, away_score, complete, processed, rules, oid)


class TableDefinition(YearRestricted):

    def __init__(self, name, order, first_year, last_year):
        self.name = name
        self.order = order

        YearRestricted.__init__(first_year, last_year)


class TableDivisionRule(YearRestricted):

    def __init__(self, table_definition, division_name, parent_division_rule, division_rank, level, first_year, last_year):
        self.table_definition = table_definition
        self.division_name = division_name
        self.parent_division_rule = parent_division_rule
        self.level = level
        self.division_rank = division_rank

        YearRestricted.__init__(first_year, last_year)


class TableTeamRule(YearRestricted):

    def __init__(self, table_definition, team, table_division_rule, first_year, last_year):
        self.table_definition = table_definition
        self.team = team
        self.table_division_rule = table_division_rule

        YearRestricted.__init__(first_year, last_year)
