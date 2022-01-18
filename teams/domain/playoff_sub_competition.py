from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from teams.domain import SubCompetition, SeriesGame
from teams.domain.sub_competition_configuration import SubCompetitionConfiguration


class PlayoffSubCompetition(SubCompetition):
    __mapper_args__ = {
        'polymorphic_identity': 'playoff_sub_competition'
    }

    current_round = Column(Integer)
    series = relationship("Series", back_populates="sub_competition")

    def __init__(self, name, series, competition, groups, order, current_round, setup, started, finished, post_processed,
                 oid=None):
        if series is None:
            self.series = []
        else:
            self.series = series
        self.current_round = current_round

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.PLAYOFF_TYPE, competition, groups, order,
                                setup, started, finished, post_processed, oid)

    def start(self):
        self.current_round = 1
        if not self.is_round_setup(self.current_round):
            self.setup_round(self.current_round)

    def post_process(self, **kwargs):
        # at this point all rounds have been processed and teams assigned to groups.
        pass

    def process_game(self, game):
        if game.complete and not game.processed:
            series = game.series
            series.process_game(game)
            game.processed = True

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

