from abc import ABC, abstractmethod

from teams.domain.competition_configuration import SubCompetitionConfiguration
from teams.domain.game import Game
from teams.domain.record import Record

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

    def __init__(self, name, records, competition, setup, started, finished, post_processed, oid):
        self.records = records

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.TABLE_TYPE, competition, setup, started, finished, post_processed,
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

    def __init__(self, name, series, competition, setup, started, finished, post_processed, oid):
        self.series = series

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.PLAYOFF_TYPE, competition, setup, started, finished, post_processed, oid)

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

    def __init__(self, series, game_number, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete, processed,
                 rules, oid):
        self.series = series
        self.game_number = game_number

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


