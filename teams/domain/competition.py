from abc import ABC, abstractmethod

from teams.domain.competition_configuration import SubCompetitionConfiguration
from teams.domain.game import Game
from teams.domain.record import Record

from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


class Competition:

    def __init__(self, name, year, sub_competitions, setup, started, finished, post_processed, oid=None):
        self.name = name
        self.year = year
        self.setup = setup
        self.started = started
        self.sub_competitions = sub_competitions
        self.finished = finished
        self.post_processed = post_processed
        self.oid = IDHelper.get_id(oid)

    @staticmethod
    def process_game(game):
        sub_comp = game.sub_competition.process_game(game)
        sub_comp.process_game(game)


class SubCompetition(ABC):

    def __init__(self, name, sub_competition_type, competition, order, setup, started, finished, post_processed, oid=None):
        self.name = name
        self.sub_competition_type = sub_competition_type
        self.competition = competition
        self.order = order
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        self.oid = IDHelper.get_id(oid)

    @abstractmethod
    def process_game(self, game):
        pass

    @abstractmethod
    def create_new_games(self, **kwargs):
        pass

    @abstractmethod
    def is_complete(self, **kwargs):
        pass


class TableSubCompetition(SubCompetition):

    def __init__(self, name, records, competition, order, setup, started, finished, post_processed, oid=None):
        self.records = records

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.TABLE_TYPE, competition, order, setup, started,
                                finished, post_processed,
                                oid)

    def process_game(self, game):
        if game.complete and not game.processed:
            home_record = [r for r in self.records if r.team.oid == game.home_team.oid][0]
            away_record = [r for r in self.records if r.team.oid == game.away_team.oid][0]

            home_record.process_game(game.home_score, game.away_score)
            away_record.prorces_game(game.away_score, game.home_score)

    def create_new_games(self):
        pass

    def is_complete(self, incomplete_games):
        if incomplete_games is None or len(incomplete_games) == 0:
            return True
        else:
            return False

    @staticmethod
    def get_dictionary_of_team_records(records):
        team_record_dict = {}
        for r in records:
            team_record_dict[r.team.oid] = r

        return team_record_dict

    @staticmethod
    # one day we need to be able to apply ranking rules, like top in each division or something like that
    def sort_rankings(team_rankings, records):
        #  sort the teams into their groups
        ranking_group_dict = TableSubCompetition.get_dictionary_of_groups_from_rankings(team_rankings)
        TableSubCompetition.sort_records_default(records)
        #  sort the records with the team id as the key
        team_record_dict = TableSubCompetition.get_dictionary_of_team_records(records)

        for group in ranking_group_dict.keys():
            #  set the team ranking to the same as their record ranking
            for team_ranking in group:
                team_ranking.rank = team_record_dict[team_ranking.team.oid]
            #  starting at 1 for the group
            group.sort(key=lambda team_rank: team_rank.rank)
            rank = 1
            for ranking in group:
                ranking.rank = rank
                rank += 1


class PlayoffSubCompetition(SubCompetition):

    def __init__(self, name, series, competition, order, current_round, setup, started, finished, post_processed, oid=None):
        self.series = series
        self.current_round = current_round

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.PLAYOFF_TYPE, competition, order, setup, started,
                                finished, post_processed, oid=None)

    def process_game(self, game):
        if game.complete and not game.processed:
            series = game.series
            series.process_game(game)

    # dictionaries of the series id and how many complete and incomplete games there are
    def create_new_games(self, complete_games_by_series, incomplete_games_by_series):
        new_games = []
        for series in [s for s in self.series if s.series_round == self.current_round]:
            new_games.extend(series.get_new_games(complete_games_by_series[series.oid],
                                                  incomplete_games_by_series[series.oid]))

        return new_games

    def is_complete(self):
        incomplete_series = [s for s in self.series if not s.is_complete()]
        if incomplete_series is None or len(incomplete_series) == 0:
            return True
        else:
            return False

    def create_series_map(self, games):
        complete_string = "Complete Games"
        incomplete_string = "Incomplete Games"

        game_status_map = {
            complete_string: {},
            incomplete_string: {}
        }
        for s in self.series:
            series_games = [g for g in games if g.series.oid == s.oid]
            game_status_map[complete_string][s.oid] = len([g for g in series_games if g.complete and g.processed])
            game_status_map[incomplete_string][s.oid] = len([g for g in series_games if not (g.complete and g.processed)])

        return game_status_map

    def is_round_complete(self, round_number):
        series = [s for s in self.series if s.series_round == round_number]

        if series is None or len(series) == 0:
            return False

        return len([s for s in series if not s.is_complete()]) == 0

    def is_round_post_processed(self, round_number):
        for s in self.series:
            if s.series_round == round_number and not s.post_processed:
                return False

        return True

    def is_round_setup(self, round_number):
        for s in self.series:
            if not s.setup and s.setup == round_number:
                return False

        return True

    def setup_round(self, round_number):
        i = 1
        if not self.is_round_setup(round_number):
            can_setup = True
            while i < round_number:
                #  if a previous round is not complete and processed, we can't set this one up
                if not self.is_round_complete(i) and self.is_round_post_processed(i):
                    can_setup = False

            if can_setup:
                series = [s for s in self.series if s.series_round == round_number]
                for s in series:
                    s.home_team = group_map[s.home_team_from]


class CompetitionTeam(Team):

    def __init__(self, competition, parent_team, oid=None):
        self.competition = competition
        self.parent_team = parent_team

        Team.__init__(self, parent_team.name, parent_team.skill, True, oid)


class CompetitionGame(Game):

    def __init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete,
                 game_processed, rules, oid=None):
        self.sub_competition = sub_competition
        self.competition = competition

        Game.__init__(self, competition.year, day, home_team, away_team, home_score, away_score, complete,
                      game_processed, rules,
                      oid)


class SeriesGame(CompetitionGame):

    def __init__(self, series, game_number, competition, sub_competition, day, home_team, away_team, home_score,
                 away_score, complete, processed,
                 rules, oid=None):
        self.series = series
        self.game_number = game_number

        CompetitionGame.__init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score,
                                 complete, processed,
                                 rules, oid)


class CompetitionGroup:

    def __init__(self, name, parent_group, sub_competition, rankings, group_type, oid=None):
        self.name = name
        self.parent_group = parent_group
        self.sub_competition = sub_competition
        self.group_type = group_type
        self.rankings = rankings
        self.oid = IDHelper.get_id(oid)

    def add_team_to_group(self, competition_team, rank):
        self.rankings.append(CompetitionRanking(self, competition_team, rank))

    def get_team_by_rank(self, rank):
        return [t for t in self.rankings if t.rank == rank][0]


class CompetitionRanking:

    def __init__(self, competition_group, competition_team, rank, oid=None):
        self.group = competition_group
        self.team = competition_team
        self.rank = rank
        self.oid = IDHelper.get_id(oid)

    @staticmethod
    def get_dictionary_of_groups_from_rankings(competition_rankings):
        ranking_group_dict = {}

        for tr in competition_rankings:
            if tr.competition_group.name not in ranking_group_dict:
                ranking_group_dict[tr.competition_group.name] = []

            ranking_group_dict[tr.tr.competition_group.name].append(tr)

        return ranking_group_dict


class TableRecords(Record):

    def __init__(self, sub_competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid=None):
        self.sub_competition = sub_competition

        Record.__init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid)
