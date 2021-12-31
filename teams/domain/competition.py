from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.game import Game
from teams.domain.record import Record

from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


class Competition(Base):
    __tablename__ = "competitions"

    oid = Column(String, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    current_round = Column(Integer)
    setup = Column(Boolean)
    started = Column(Boolean)
    finished = Column(Boolean)
    post_processed = Column(Boolean)

    def __init__(self, name, year, sub_competitions, teams, current_round, setup, started, finished, post_processed,
                 oid=None):
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
        in_complete_sub_comps = [s for s in self.sub_competitions if s.order == round_number and (
                    not s.started or not s.setup or not s.finished or not s.post_processed)]
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

    def __eq__(self, other):
        return self.oid == other.oid and \
               self.name == other.name and \
               self.current_round == other.current_round and \
               self.setup == other.setup and \
               self.started == other.started and \
               self.finished == other.finished and \
               self.post_processed == other.post_processed
