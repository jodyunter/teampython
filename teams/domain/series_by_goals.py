from sqlalchemy import Column, Integer

from teams.domain.series import Series
from teams.domain.series_game import SeriesGame
from teams.domain.series_rules import SeriesRules


class SeriesByGoals(Series):
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    games_played = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_goals'
    }

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
                          self.sub_competition, -1, self.get_home_team_for_game(game_number),
                          self.get_away_team_for_game(game_number),
                          0, 0, False, False, game_rules)
