from abc import ABC, abstractmethod

from teams.domain.game import Game
from teams.domain.record import Record
from teams.domain.series_rules import SeriesRules
from teams.domain.team import Team


class Competition:

    def __init__(self, name, year, sub_competitions, setup, started, finished, post_processed, oid):
        self.name = name
        self.year = year
        self.setup = setup
        self.started = started
        self.sub_competitions = sub_competitions
        self.finished = finished
        self.post_processed = post_processed
        self.oid = oid

    @staticmethod
    def process_game(game):
        sub_comp = game.sub_competition.process_game(game)
        sub_comp.process_game(game)


class SubCompetition(ABC):

    def __init__(self, name, sub_competition_type, competition, setup, started, finished, post_processed, oid):
        self.name = name
        self.sub_competition_type = sub_competition_type
        self.competition = competition
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        self.oid = oid

    @abstractmethod
    def process_game(self, game):
        pass

    @abstractmethod
    def create_new_games(self, game_creation_method):
        pass

    @abstractmethod
    def is_complete(self, **kwargs):
        pass


class TableSubCompetition(SubCompetition):

    def __init__(self, name, sub_competition_type, records, competition, setup, started, finished, post_processed, oid):
        self.records = records

        SubCompetition.__init__(self, name, sub_competition_type, competition, setup, started, finished, post_processed,
                                oid)

    def process_game(self, game):
        if game.complete and not game.processed:
            home_record = [r for r in self.records if r.team.oid == game.home_team.oid][0]
            away_record = [r for r in self.records if r.team.oid == game.away_team.oid][0]

            home_record.process_game(game.home_score, game.away_score)
            away_record.prorces_game(game.away_score, game.home_score)

    def create_new_games(self, game_creation_method):
        pass

    def is_complete(self, incomplete_games):
        if incomplete_games is None or len(incomplete_games) == 0:
            return True
        else:
            return False

    # one day we need to be able to apply ranking rules, like top in each division or something like that
    def sort_records(self, team_rankings, records):
        count = 0
        ranking_group_dict = {}
        for tr in team_rankings:
            if tr.competition_group.name not in ranking_group_dict:
                ranking_group_dict[tr.competition_group.name] = []

            ranking_group_dict[tr.tr.competition_group.name].append(tr)

        for r in records.sort(key=lambda rec: (-rec.points, -rec.wins, rec.games, -rec.goal_difference)):
            r.rank = count
            count += 1

        team_record_dict = {}

        for r in records:
            team_record_dict[r.team.oid] = r

        for group in ranking_group_dict.keys():
            pass


class PlayoffSubCompetition(SubCompetition):

    def __init__(self, name, sub_competition_type, series, competition, setup, started, finished, post_processed, oid):
        self.series = series

        SubCompetition.__init__(self, name, sub_competition_type, competition, setup, started, finished, post_processed, oid)

    def process_game(self, game):
        if game.complete and not game.processed:
            series = game.series
            series.process_game(game)

    def create_new_games(self, game_creation_method):
        pass

    def is_complete(self, incomplete_series):
        if incomplete_series is None or len(incomplete_series) == 0:
            return True
        else:
            return False


class CompetitionTeam(Team):

    def __init__(self, competition, parent_team, oid):
        self.competition = competition
        self.parent_team = parent_team

        Team.__init__(self, parent_team.name, parent_team.skill, True, oid)


class CompetitionGame(Game):

    def __init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete, game_processed, rules, oid):
        self.sub_competition = sub_competition

        Game.__init__(self, competition.year, day, home_team, away_team, home_score, away_score, complete, game_processed, rules,
                      oid)


class SeriesGame(CompetitionGame):

    def __init__(self, series, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete, processed,
                 rules, oid):
        self.series = series

        CompetitionGame.__init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete, processed,
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


class Series(ABC):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, series_type, series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
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
        self.setup = setup
        self.post_processed = post_processed
        self.oid = oid

    @abstractmethod
    def process_game(self, game):
        pass

    @abstractmethod
    def is_complete(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def get_loser(self):
        pass

    # we could add a check on the game if it is one of the two teams
    def can_process_game(self, game):
        return game.complete and not game.processed and not self.is_complete()


class SeriesByWins(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_wins, away_wins,
                 series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
                 oid):
        self.home_wins = home_wins
        self.away_wins = away_wins

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.WINS_TYPE, series_rules, game_rules,
                        home_team_from_group, home_team_value,
                        away_team_from_group, away_team_value,
                        winner_to_group, winner_rank_from,
                        loser_to_group, loser_rank_from,
                        setup, post_processed,
                        oid)

    def process_game(self, game):
        if self.can_process_game(game):
            if game.get_winner().oid == self.home_team.oid:
                self.home_wins += 1
            elif game.get_winner().oid == self.away_team.oid:
                self.away_wins += 1

            game.processed = True

    def is_complete(self):
        return self.series_rules.required_wins == self.home_wins or self.series_rules.required_wins == self.away_wins

    def get_winner(self):
        if self.is_complete():
            required_wins = self.series_rules.required_wins

            if self.home_wins == required_wins:
                return self.home_team
            elif self.away_wins == required_wins:
                return self.away_team

        return None

    def get_loser(self):
        if self.is_complete():
            required_wins = self.series_rules.required_wins

            if self.home_wins == required_wins:
                return self.away_team
            elif self.away_wins == required_wins:
                return self.home_team

        return None


class SeriesByGoals(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_goals, away_goals, games_played,
                 series_rules, game_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
                 oid):
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.games_played = games_played

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.GOALS_TYPE, series_rules, game_rules,
                        home_team_from_group, home_team_value,
                        away_team_from_group, away_team_value,
                        winner_to_group, winner_rank_from,
                        loser_to_group, loser_rank_from,
                        setup, post_processed,
                        oid)

    def process_game(self, game):
        if self.can_process_game(game):
            self.home_goals += game.home_score
            self.away_goals += game.away_score
            game.processed = True
            self.games_played += 1

    def is_complete(self):
        return self.series_rules.games_to_play == self.games_played and self.home_goals != self.away_goals

    def get_winner(self):
        if self.is_complete():
            if self.home_goals > self.away_goals:
                return self.home_team
            elif self.away_goals > self.home_goals:
                return self.away_team

        return None

    def get_loser(self):
        if self.is_complete():
            if self.home_goals > self.away_goals:
                return self.away_team
            elif self.away_goals > self.home_goals:
                return self.home_team

        return None