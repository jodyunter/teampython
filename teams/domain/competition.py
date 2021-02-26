from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import Game
from teams.domain.record import Record

from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


class Competition:

    def __init__(self, name, year, sub_competitions, teams, setup, started, finished, post_processed, oid=None):
        self.name = name
        self.year = year
        self.setup = setup
        self.started = started
        self.sub_competitions = sub_competitions
        self.teams = teams
        self.finished = finished
        self.post_processed = post_processed
        self.oid = IDHelper.get_id(oid)

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


class RankingGroup(CompetitionGroup):

    def __init__(self, name, parent_group, sub_competition, level, rankings, oid=None):
        CompetitionGroup.__init__(self, name, parent_group, sub_competition, level, rankings, CompetitionGroupConfiguration.RANKING_TYPE, oid)


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


class TableRecord(Record):

    def __init__(self, sub_competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid=None):
        self.sub_competition = sub_competition

        Record.__init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid)
