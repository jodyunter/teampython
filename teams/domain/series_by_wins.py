# TODO: Implement the home pattern.
from sqlalchemy import Column, Integer

from teams.domain.series import Series
from teams.domain.series_rules import SeriesRules


class SeriesByWins(Series):
    home_wins = Column(Integer)
    away_wins = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins'
    }

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
