from abc import ABC, abstractmethod

from sqlalchemy import Integer, Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.series_game import SeriesGame
from teams.domain.series_rules import SeriesRules
from teams.domain.utility.utility_classes import IDHelper


class Series(Base, ABC):
    __tablename__ = "series"

    oid = Column(String, primary_key=True)
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("PlayoffSubCompetition", foreign_keys=[sub_competition_id])
    name = Column(String)
    series_round = Column(Integer)
    home_team_id = Column(String, ForeignKey('teams.oid'))
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team_id = Column(String, ForeignKey('teams.oid'))
    away_team = relationship("Team", foreign_keys=[away_team_id])
    series_type = Column(String)
    series_rules_id = Column(String, ForeignKey('seriesrules.oid'))
    series_rules = relationship("SeriesRules", foreign_keys=[series_rules_id])
    home_team_from_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    home_team_from_group = relationship("CompetitionGroup", foreign_keys=[home_team_from_group_id])
    home_team_value = Column(Integer)
    away_team_from_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    away_team_from_group = relationship("CompetitionGroup", foreign_keys=[away_team_from_group_id])
    away_team_value = Column(Integer)
    winner_to_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    winner_to_group = relationship("CompetitionGroup", foreign_keys=[winner_to_group_id])
    loser_to_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    loser_to_group = relationship("CompetitionGroup", foreign_keys=[loser_to_group_id])
    setup = Column(Boolean)
    post_processed = Column(Boolean)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'series'
    }

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
                          self.sub_competition, -1,
                          self.get_home_team_for_game(game_number),
                          self.get_away_team_for_game(game_number),
                          0, 0, False, False, self.series_rules.game_rules)

    # we could add a check on the game if it is one of the two teams
    def can_process_game(self, game, ):
        return game.complete and not game.processed and not self.is_complete()

    def get_home_pattern_value(self, game_number):
        index_num = game_number - 1
        if self.series_rules.home_pattern is None or game_number > len(self.series_rules.home_pattern):
            value = index_num % 2
        else:
            value = self.series_rules.home_pattern[index_num]

        return value

    def get_home_team_for_game(self, game_number):
        value = self.get_home_pattern_value(game_number)

        if value % 2 == 0:
            return self.home_team
        else:
            return self.away_team

    def get_away_team_for_game(self, game_number):
        value = self.get_home_pattern_value(game_number)

        if value % 2 == 0:
            return self.away_team
        else:
            return self.home_team
