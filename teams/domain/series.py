from abc import ABC, abstractmethod

from teams.domain.competition import SeriesGame
from teams.domain.series_rules import SeriesRules
from teams.domain.utility.utility_classes import IDHelper


class Series(ABC):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, series_type, series_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
                 oid=None):
        self.sub_competition = sub_competition
        self.name = name
        self.series_round = series_round
        self.home_team = home_team
        self.away_team = away_team
        self.series_type = series_type
        self.series_rules = series_rules
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
        self.oid = IDHelper.get_id(oid)

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

    @abstractmethod
    def get_new_games(self, complete_games, incomplete_games):
        pass

    def create_game(self, game_number):
        return SeriesGame(self, game_number, self.sub_competition.competition,
                          self.sub_competition, -1, self.home_team, self.away_team,
                          0, 0, False, False, self.series_rules.game_rules)

    # we could add a check on the game if it is one of the two teams
    def can_process_game(self, game, ):
        return game.complete and not game.processed and not self.is_complete()


# TODO: Implement the home pattern.
class SeriesByWins(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_wins, away_wins,
                 series_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
                 oid=None):
        self.home_wins = home_wins
        self.away_wins = away_wins

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.WINS_TYPE, series_rules,
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

    def get_new_games(self, complete_games, incomplete_games):

        if self.home_wins >= self.away_wins:
            closest_to_winning = self.home_wins
        else:
            closest_to_winning = self.away_wins

        required_wins = self.series_rules.required_wins - closest_to_winning
        required_games = required_wins - incomplete_games

        last_game_number = complete_games + incomplete_games

        new_games = []

        for i in range(required_games):
            last_game_number += 1
            new_games.append(self.create_game(last_game_number))

        return new_games


class SeriesByGoals(Series):

    def __init__(self, sub_competition, name, series_round, home_team, away_team, home_goals, away_goals, games_played,
                 series_rules,
                 home_team_from_group, home_team_value,
                 away_team_from_group, away_team_value,
                 winner_to_group, winner_rank_from,
                 loser_to_group, loser_rank_from,
                 setup, post_processed,
                 oid=None):
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.games_played = games_played

        Series.__init__(self, sub_competition, name, series_round, home_team, away_team,
                        SeriesRules.GOALS_TYPE, series_rules,
                        home_team_from_group, home_team_value,
                        away_team_from_group, away_team_value,
                        winner_to_group, winner_rank_from,
                        loser_to_group, loser_rank_from,
                        setup, post_processed,
                        oid)

    # this setup isn't really fair
    # TODO: make this more fair.  The last game shouldn't automatically go to overtime.  Maybe we just keep making games as needed
    def process_game(self, game):
        if self.can_process_game(game):
            self.home_goals += game.home_score
            self.away_goals += game.away_score
            game.processed = True
            self.games_played += 1

    def is_complete(self):
        return self.series_rules.games_to_play <= self.games_played and self.home_goals != self.away_goals

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

    def get_new_games(self, complete_games, incomplete_games):
        total_games = complete_games + incomplete_games
        new_games = []
        minimum_games = self.series_rules.games_to_play

        #  this will create any missing games
        while total_games < minimum_games:
            total_games += 1
            new_games.append(self.create_game(total_games))

        # if all games are complete, and the goals are tied, create a new game with the special last rules
        if complete_games == minimum_games and self.home_goals == self.away_goals:
            new_games.append(self.create_game(total_games + 1))

        return new_games

    def create_game(self, game_number):
        game_rules = self.series_rules.game_rules
        if game_number > self.series_rules.games_to_play:
            game_rules = self.series_rules.last_game_rules

        return SeriesGame(self, game_number, self.sub_competition.competition,
                          self.sub_competition, -1, self.home_team, self.away_team,
                          0, 0, False, False, game_rules)
