from random import Random

from teams.data.repo.game_repository import GameRepository
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.game import Game, GameRules
from teams.domain.scheduler import Scheduler
from teams.services.base_service import BaseService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from teams.services.view_models.game_view_models import GameViewModel, GameRulesViewModel


class GameRulesService(BaseService):
    repo = GameRulesRepository()

    def create(self, name, can_tie, session=None):
        if session is None:
            session = self.repo.get_session()
        self.repo.add(GameRules(name, can_tie, self.get_new_id()), session)
        session.commit()

    def get_by_name(self, name, session=None):
        if session is None:
            session = self.repo.get_session()

        rules = self.repo.get_by_name(name, session)
        return GameRulesViewModel(rules.oid, rules.name, rules.can_tie)


class GameService(BaseService):
    team_service = TeamService()
    record_service = RecordService()
    repo = GameRepository()
    team_repo = TeamRepository()
    record_repo = RecordRepository()
    game_rules_repo = GameRulesRepository()

    def create_game_from_schedule_game(self, schedule_game, session=None):
        commit = False
        if session is None:
            session = self.repo.get_session()
            commit = True

        team_a = self.team_repo.get_by_oid(schedule_game.home_id, session)
        team_b = self.team_repo.get_by_oid(schedule_game.away_id, session)
        rules = self.game_rules_repo.get_by_oid(schedule_game.rules_id, session)

        if team_a is None:
            raise AttributeError("Team A cannot be none.")
        if team_b is None:
            raise AttributeError("Team B cannot be none.")

        game = Game(schedule_game.year, schedule_game.day, team_a, team_b, 0, 0, False, False, rules, self.get_new_id())

        if commit:
            session.Commit()

        return game

    def create_games(self, team_list, year, start_day, rules, home_and_away, session=None):
        if session is None:
            session = self.repo.get_session()

        game_list = []

        scheduler = Scheduler()
        team_ids = [i.oid for i in team_list]

        schedule_games = scheduler.schedule_games(team_ids, rules.oid, year, start_day, home_and_away)
        new_games = [self.create_game_from_schedule_game(sg, session) for sg in schedule_games]
        [self.repo.add(g, session) for g in new_games]

        session.commit()

    @staticmethod
    def game_to_vm(g):
        return GameViewModel(g.oid, g.year, g.day, g.home_team.name, g.home_team.oid,
                             g.away_team.name, g.away_team.oid, g.home_score,
                             g.away_score, g.complete)

    def get_all_games(self):
        session = self.repo.get_session()
        return [self.game_to_vm(g) for g in self.repo.get_all(session)]

    def play_game(self, game_list, random):
        session = self.repo.get_session()

        for g in game_list:
            game = self.repo.get_by_oid(g.oid, session)
            game.play(random)

        session.commit()

    def get_games_to_process(self, session=None):
        if session is None:
            session = self.repo.get_session()

        return self.repo.get_by_unprocessed_and_complete(session)

    def process_games(self):
        session = self.repo.get_session()
        game_list = list(self.get_games_to_process(session))

        for g in game_list:
            home_record = self.record_repo.get_by_team_and_year(g.home_team.oid, g.year, session)
            away_record = self.record_repo.get_by_team_and_year(g.away_team.oid, g.year, session)

            home_record.process_game(g.home_score, g.away_score)
            away_record.process_game(g.away_score, g.home_score)

            self.record_service.update_records([home_record, away_record], session)

        session.commit()
