from teams.domain.game import Game
from teams.domain.record import Record
from teams.domain.series_rules import SeriesRules
from teams.domain.team import Team


class Competition:

    def __init__(self, name, year, setup, started, finished, post_processed, oid):
        self.name = name
        self.year = year
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        self.oid = oid


class SubCompetition:

    def __init__(self, name, sub_competition_type, competition, setup, started, finished, post_processed, oid):
        self.name = name
        self.sub_competition_type = sub_competition_type
        self.competition = competition
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        self.oid = oid


class CompetitionTeam(Team):

    def __init__(self, competition, parent_team, name, skill, oid):
        self.competition = competition
        self.parent_team = parent_team

        Team.__init__(self, name, skill, True, oid)


class CompetitionGame(Game):

    def __init__(self, competition, day, home_team, away_team, home_score, away_score, complete, processed, rules, oid):
        Game.__init__(self, competition.year, day, home_team, away_team, home_score, away_score, complete, processed, rules,
                      oid)


class SeriesGame(CompetitionGame):

    def __init__(self, series, competition, day, home_team, away_team, home_score, away_score, complete, processed,
                 rules, oid):
        self.series = series

        CompetitionGame.__init__(self, competition, day, home_team, away_team, home_score, away_score, complete, processed,
                                 rules, oid)


class CompetitionGroup:

    def __init__(self, name, parent_group, sub_competition, group_type, oid):
        self.name = name
        self.parent_group = parent_group
        self.sub_competition = sub_competition
        self.group_type = group_type
        self.oid = oid


class CompetitionRanking:

    def __init__(self, competition_group, competition_team, rank, oid):
        self.competition_group = competition_group
        self.competition_team = competition_team,
        self.rank = rank
        self.oid = oid


class TableRecords(Record):

    def __init__(self, sub_competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid):
        self.sub_competition = sub_competition

        Record.__init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid)


class Series:

    def __init__(self, sub_competition, name, series_round, home_team, away_team, series_type, series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 oid):
        self.sub_competition = sub_competition
        self.name = name
        self.series_round = series_round
        self.home_team = home_team
        self.away_team = away_team
        self.series_type = series_type
        self.series_rules = series_rules
        self.game_rules = game_rules
        self.home_team_from_group = home_team_from_group
        self.home_team_value = home_team_value
        self.away_team_from_group = away_team_from_group
        self.away_team_value = away_team_value
        self.winner_to_group = winner_to_group
        self.winner_rank_from = winner_rank_from
        self.loser_to_group = loser_to_group
        self.loser_rank_from = loser_rank_from
        self.oid = oid


class SeriesByWins(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_wins, away_wins,
                 series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 oid):
        self.home_wins = home_wins
        self.away_wins = away_wins

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.WINS_TYPE, series_rules, game_rules,
                        home_team_from_group, home_team_value,
                        away_team_from_group, away_team_value,
                        winner_to_group, winner_rank_from,
                        loser_to_group, loser_rank_from,
                        oid)


class SeriesByGoals(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_goals, away_goals,
                 series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 oid):
        self.home_goals = home_goals
        self.away_goals = away_goals

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.GOALS_TYPE, series_rules, game_rules,
                        home_team_from_group, home_team_value,
                        away_team_from_group, away_team_value,
                        winner_to_group, winner_rank_from,
                        loser_to_group, loser_rank_from,
                        oid)
