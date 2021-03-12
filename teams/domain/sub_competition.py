from abc import ABC, abstractmethod

from teams.domain.competition import TableRecord, CompetitionRanking, CompetitionGame
from teams.domain.competition_configuration import SubCompetitionConfiguration
from teams.domain.series import SeriesGame
from teams.domain.utility.utility_classes import IDHelper


class SubCompetition(ABC):

    def __init__(self, name, sub_competition_type, competition, groups, order, setup, started, finished, post_processed,
                 oid=None):
        self.name = name
        self.sub_competition_type = sub_competition_type
        self.competition = competition
        self.order = order
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        self.groups = groups
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

    @abstractmethod
    def post_process(self, **kwargs):
        pass

    @abstractmethod
    def process_end_of_day(self):
        pass

    def get_groups_by_level(self, level):
        return [g for g in self.groups if g.level == level]

    def get_group_by_name(self, name):
        groups = [g for g in self.groups if g.name == name]
        if groups is None or len(groups) == 0:
            return []
        else:
            return groups[0]


class TableSubCompetition(SubCompetition):

    def post_process(self, **kwargs):
        # do a final sort
        self.sort_table_rankings()
        # add users to any special groups (champion, division champions, or whatever)

    def __init__(self, name, records, competition, groups, order, setup, started, finished, post_processed, oid=None):
        self.records = records

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.TABLE_TYPE, competition, groups, order, setup, started,
                                finished, post_processed,
                                oid)

    def process_end_of_day(self):
        pass

    def create_game(self, home, away, rules, year, day):
        return CompetitionGame(self.competition, self, day, home, away, 0, 0, False, False, rules)

    def process_game(self, game):
        if game.complete and not game.processed:
            home_record = [r for r in self.records if r.team.oid == game.home_team.oid][0]
            away_record = [r for r in self.records if r.team.oid == game.away_team.oid][0]

            home_record.process_game(game.home_score, game.away_score)
            away_record.process_game(game.away_score, game.home_score)

    # TODO:  this will need the configuration.
    # We should only create new games when previous round of sub comps is done.  This way the previous comps populate groups that we'll use to create games
    def create_new_games(self, **kwargs):
        return None

    def is_complete(self, **kwargs):
        incomplete_games = kwargs.get("incomplete_games", None)

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

    def sort_table_rankings(self):
        rankings = []
        for group in self.groups:
            rankings.extend(group.rankings)

        self.sort_rankings(rankings, self.records)

    @staticmethod
    # one day we need to be able to apply ranking rules, like top in each division or something like that
    def sort_rankings(team_rankings, records):
        #  sort the teams into their groups
        ranking_group_dict = CompetitionRanking.get_dictionary_of_groups_from_rankings(team_rankings)
        TableRecord.sort_records_default(records)
        #  sort the records with the team id as the key
        team_record_dict = TableSubCompetition.get_dictionary_of_team_records(records)

        for group_name in ranking_group_dict.keys():
            group = ranking_group_dict[group_name]
            #  set the team ranking to the same as their record ranking
            for team_ranking in group:
                team_ranking.rank = team_record_dict[team_ranking.team.oid].rank
            #  starting at 1 for the group
            group.sort(key=lambda team_rank: team_rank.rank)
            rank = 1
            for ranking in group:
                ranking.rank = rank
                rank += 1

    @staticmethod
    def get_records_by_group(ranking_group, table_records):
        return TableSubCompetition.get_records_by_team([r for r in ranking_group.rankings], table_records)

    @staticmethod
    def get_records_by_team(rankings, table_records):
        result = []
        for t in rankings:
            record = [r for r in table_records if r.team.oid == t.team.oid][0]
            record.rank = t.rank
            result.append(record)

        return result


class PlayoffSubCompetition(SubCompetition):

    def post_process(self, **kwargs):
        # at this point all rounds have been processed and teams assigned to groups.
        pass

    def __init__(self, name, series, competition, groups, order, current_round, setup, started, finished, post_processed,
                 oid=None):
        self.series = series
        self.current_round = current_round

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.PLAYOFF_TYPE, competition, groups, order,
                                setup, started, finished, post_processed, oid)

    def process_game(self, game):
        if game.complete and not game.processed:
            series = game.series
            series.process_game(game)

    # dictionaries of the series id and how many complete and incomplete games there are
    def create_new_games(self, **kwargs):
        current_games = kwargs["current_games"]
        game_status_map = self.create_series_map(current_games)
        new_games = []
        for series in [s for s in self.series if s.series_round == self.current_round]:
            new_games.extend(series.get_new_games(game_status_map["Complete Games"][series.oid],
                                                  game_status_map["Incomplete Games"][series.oid]))

        for g in new_games:
            g.sub_competition = self

        return new_games

    def is_complete(self, **kwargs):
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
            series_games = [g for g in games if isinstance(g, SeriesGame) and g.series.oid == s.oid]
            game_status_map[complete_string][s.oid] = len([g for g in series_games if g.complete and g.processed])
            game_status_map[incomplete_string][s.oid] = len(
                [g for g in series_games if not (g.complete and g.processed)])

        return game_status_map

    def is_round_complete(self, round_number):
        series_for_round = self.get_series_for_round(round_number)

        if series_for_round is None or len(series_for_round) == 0:
            return False

        return len([s for s in series_for_round if not s.is_complete()]) == 0

    def is_round_post_processed(self, round_number):
        for s in self.series:
            if s.series_round == round_number and not s.post_processed:
                return False

        return True

    def is_round_setup(self, round_number):
        for s in self.series:
            if not s.setup and s.series_round == round_number:
                return False

        return True

    def post_process_round(self, round_number):
        if self.is_round_complete(round_number):
            series_for_round = self.get_series_for_round(round_number)

            for s in series_for_round:
                self.add_team_to_group(s.get_winner(), s.winner_to_group, s.winner_rank_from)
                self.add_team_to_group(s.get_loser(), s.loser_to_group, s.loser_rank_from)
                s.post_processed = True
            #  setup grabs the team from the groups

    @staticmethod
    def add_team_to_group(team, group, group_with_rank):
        # TODO: need to make this better
        if team is None or group is None or group_with_rank is None:
            return
        else:
            group.add_team_to_group(team, group_with_rank.get_rank_for_team(team))

    #  setup makes sure the round can be setup
    def setup_round(self, round_number):
        i = 1
        if not self.is_round_setup(round_number):
            can_setup = True
            while i < round_number:
                #  if a previous round is not complete and processed, we can't set this one up
                if not self.is_round_complete(i) and self.is_round_post_processed(i):
                    can_setup = False
                i += 1

            if can_setup:
                series = [s for s in self.series if s.series_round == round_number]
                for s in series:
                    if not s.setup:
                        #  get by order in case the groups haven't been ranked from 1
                        s.home_team = s.home_team_from_group.get_team_by_order(s.home_team_value).team
                        s.away_team = s.away_team_from_group.get_team_by_order(s.away_team_value).team
                        s.setup = True

    def get_series_for_round(self, round_number):
        return [s for s in self.series if s.series_round == round_number]

    def process_end_of_day(self):
        if self.is_round_complete(self.current_round):
            self.post_process_round(self.current_round)
            self.current_round += 1
            if not self.is_round_setup(self.current_round):
                self.setup_round(self.current_round)
