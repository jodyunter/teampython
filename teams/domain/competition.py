from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import Game
from teams.domain.record import Record

from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


class Competition:

    def __init__(self, name, year, sub_competitions, teams, current_round, setup, started, finished, post_processed, oid=None):
        self.name = name
        self.year = year
        self.setup = setup
        self.started = started
        self.sub_competitions = sub_competitions
        self.teams = teams
        self.finished = finished
        self.post_processed = post_processed
        self.oid = IDHelper.get_id(oid)
        self.current_round = current_round

    def create_new_games(self, **kwargs):
        games = []
        for sub in self.get_started_but_not_finished_comps(self.current_round):
            result = sub.create_new_games(**kwargs)
            if result is not None:
                games.extend(result)
        return games

    @staticmethod
    def process_game(game):
        game.sub_competition.process_game(game)

    def get_groups_by_level_and_comp(self, level, comp_name):
        sc = self.get_sub_competition(comp_name)
        return sc.get_groups_by_level(level)

    def get_group_by_name(self, name):
        for s in self.sub_competitions:
            for g in s.groups:
                if g.name == name:
                    return g

        return None

    def get_all_groups(self):
        current_groups = []

        for s in self.sub_competitions:
            current_groups.extend(s.groups)

        return current_groups

    def get_sub_competition(self, name):
        for s in self.sub_competitions:
            if s.name == name:
                return s

    def is_round_complete(self, round_number):
        in_complete_sub_comps = [s for s in self.sub_competitions if s.order == round_number and (not s.started or not s.setup or not s.finished or not s.post_processed)]
        return in_complete_sub_comps is None or len(in_complete_sub_comps) == 0

    # todo:  we need to figure out which sub comps are currently running, which need to be post processed, which need to be setup and which need to be started
    #  not setup means something went wrong.  All sub comps should be setup at the start
    #  started means we've created our initial games and schedule
    #  finished means all comes are done, or all series are done.
    #  post processed means we've added teams to the appropriate groups

    def get_sub_competitions_by_round(self, round_number):
        return [s for s in self.sub_competitions if s.order == round_number]

    def get_started_but_not_finished_comps(self, round_number):
        return [s for s in self.sub_competitions if not s.finished and s.started and s.order == round_number]

    def get_finished_but_not_processed_sub_comps(self, round_number):
        return [s for s in self.sub_competitions if not s.post_processed and s.finished and s.order == round_number]

    #  { sub_comp_oid : count_of_incomplete_games }
    def process_end_of_day(self, incomplete_games_by_sub_comp):
        #  get all start sub comps that are not finished
        for s in self.get_started_but_not_finished_comps(self.current_round):
            s.process_end_of_day()
            incomplete_games = None
            if s.oid in incomplete_games_by_sub_comp:
                incomplete_games = incomplete_games_by_sub_comp[s.oid]

            if s.is_complete(incomplete_games=incomplete_games):
                s.finished = True

        for s in self.get_finished_but_not_processed_sub_comps(self.current_round):
            # post process
            s.post_process()
            s.post_processed = True

        if self.is_round_complete(self.current_round):
            self.current_round += 1
            self.start_round(self.current_round)

        self.check_complete()

    def check_complete(self):
        subs = self.get_sub_competitions_by_round(self.current_round)
        if len(subs) == 0:
            self.finished = True

        return self.finished

    # this is to accommodate the table sub comp's way of saying it's complete
    # todo: this isn't great to do it this way
    def sort_day_dictionary_to_incomplete_games_dictionary(self, day_dictionary):
        incomplete_dictionary = {}
        for d in day_dictionary.keys():
            for game in day_dictionary[d]:
                sub_comp_id = game.sub_competition.oid
                if sub_comp_id not in incomplete_dictionary:
                    incomplete_dictionary[sub_comp_id] = []
                if not game.complete or not game.processed:
                    incomplete_dictionary[sub_comp_id].append(game)
        return incomplete_dictionary

    def start_competition(self):
        self.current_round = 1
        self.start_round(self.current_round)

    def start_round(self, round_number):
        subs = self.get_sub_competitions_by_round(round_number);
        for sub in subs:
            sub.start()
            sub.started = True


# mapped
class CompetitionTeam(Team):

    def __init__(self, competition, parent_team, oid=None):
        self.competition = competition
        self.parent_team = parent_team

        Team.__init__(self, parent_team.name, parent_team.skill, True, oid)

# mapped
class CompetitionGame(Game):

    def __init__(self, competition, sub_competition, day, home_team, away_team, home_score, away_score, complete,
                 game_processed, rules, oid=None):
        self.sub_competition = sub_competition
        self.competition = competition

        Game.__init__(self, competition.year, day, home_team, away_team, home_score, away_score, complete,
                      game_processed, rules,
                      oid)

# mapped
class CompetitionGroup:

    def __init__(self, name, parent_group, sub_competition, level, rankings, group_type, oid=None):
        self.name = name
        self.parent_group = parent_group
        self.sub_competition = sub_competition
        self.group_type = group_type
        self.level = level
        self.rankings = rankings
        self.oid = IDHelper.get_id(oid)

    def add_team_to_group(self, competition_team, rank=None):
        if rank is None:
            rank = -1
        team_in_group = [t for t in self.rankings if t.team.oid == competition_team.oid]
        if team_in_group is None or len(team_in_group) == 0:
            self.rankings.append(CompetitionRanking(self, competition_team, rank))
        else:
            return

    def get_rank_for_team(self, team):
        return [r.rank for r in self.rankings if r.team.oid == team.oid][0]

    def get_team_by_rank(self, rank):
        return [t for t in self.rankings if t.rank == rank][0].team

    def get_ranking_for_team(self, team):
        return [r for r in self.rankings if r.team.oid == team.oid][0]

    # assume 1 is the first
    def get_team_by_order(self, order, reverse=False):
        self.rankings.sort(key=lambda team_rank: team_rank.rank)

        return self.rankings[order - 1]

    def set_rank(self, team, rank):
        self.get_ranking_for_team(team).rank = rank


# mapped
class RankingGroup(CompetitionGroup):

    def __init__(self, name, parent_group, sub_competition, level, rankings, oid=None):
        CompetitionGroup.__init__(self, name, parent_group, sub_competition, level, rankings, CompetitionGroupConfiguration.RANKING_TYPE, oid)


# mapped
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
            if tr.group.name not in ranking_group_dict:
                ranking_group_dict[tr.group.name] = []

            ranking_group_dict[tr.group.name].append(tr)

        return ranking_group_dict


# mapped
class TableRecord(Record):

    def __init__(self, sub_competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid=None):
        self.sub_competition = sub_competition

        Record.__init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid)
