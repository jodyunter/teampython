from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.game_repository import GameRepository
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.game import Game, GameRules
from teams.domain.scheduler import Scheduler
from teams.services.base_service import BaseService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from teams.services.view_models.game_view_models import GameViewModel, GameRulesViewModel, GameDayViewModel


class GameRulesService(BaseService):
    repo = GameRulesRepository()

    def create(self, name, can_tie, session=None):
        if session is None:
            session = self.repo.get_session()
        self.repo.add(GameRules(name, can_tie, self.get_new_id()), GameRulesDTO, session)
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

        team_a = self.team_repo.get_by_oid(schedule_game.home_team, TeamDTO, session)
        team_b = self.team_repo.get_by_oid(schedule_game.home_team, TeamDTO, session)
        rules = self.game_rules_repo.get_by_oid(schedule_game.rules, GameRulesDTO, session)

        if team_a is None:
            raise AttributeError("Team A cannot be none.")
        if team_b is None:
            raise AttributeError("Team B cannot be none.")

        game = Game(schedule_game.year, schedule_game.day, team_a, team_b, 0, 0, False, False, rules, self.get_new_id())

        if commit:
            session.Commit()

        return game

    def create_games(self, team_list, year, start_day, rules, rounds, home_and_away, session=None):
        if session is None:
            session = self.repo.get_session()

        scheduler = Scheduler()
        team_ids = [i.oid for i in team_list]

        schedule_games = []
        # schedule_games = scheduler.schedule_games(team_ids, rules.oid, year, start_day, home_and_away)
        for i in range(rounds):
            schedule_games.extend(scheduler.schedule_games(team_ids, rules.oid, year, start_day, home_and_away))
            start_day = max([sg.day for sg in schedule_games])
            start_day += 1

        new_games = [self.create_game_from_schedule_game(sg, session) for sg in schedule_games]
        [self.repo.add(g, GameDTO, session) for g in new_games]

        session.commit()

    @staticmethod
    def games_to_game_day_view(games):
        game_vm = [GameService.game_to_vm(g) for g in games]
        return GameDayViewModel(None, game_vm[0].day, game_vm[0].year, game_vm)

    @staticmethod
    def game_to_vm(g):
        return GameViewModel(g.oid, g.year, g.day, g.home_team.name, g.home_team.oid,
                             g.away_team.name, g.away_team.oid, g.home_score,
                             g.away_score, g.complete)

    def get_all_games(self):
        session = self.get_session()
        return [self.game_to_vm(g) for g in self.repo.get_all(session)]

    def play_game(self, game_list, random, session=None):
        commit = session is None
        session = self.get_session(session)

        for g in game_list:
            game = self.repo.get_by_oid(g.oid, GameDTO, session)
            game.play()

        self.commit(session, commit)

    def get_games_for_days(self, year, first_day, last_day, session=None):
        commit = session is None
        session = self.get_session()

        result = self.repo.get_games_by_day(year, first_day, last_day, session)

        self.commit(session, commit)

        return [self.game_to_vm(g) for g in result]

    def play_games_for_days(self, year, first_day, last_day, random, session=None):
        commit = session is None
        session = self.get_session(session)

        games = self.repo.get_games_by_day(year, first_day, last_day, session)

        self.play_game(games, random, session)

        self.commit(session, commit)

        return [self.game_to_vm(g) for g in self.repo.get_games_by_day(year, first_day, last_day, session)]

    def get_incomplete_games_for_days(self, year, first_day, last_day, session=None):
        session = self.get_session(session)
        return [self.game_to_vm(g)
                for g in self.repo.get_incomplete_or_unprocessed_games_by_day(year, first_day, last_day, session)]

    def get_complete_and_unprocessed_games_for_days(self, year, first_day, last_day, session=None):
        session = self.get_session(session)

        return [self.game_to_vm(g)
                for g in self.repo.get_by_unprocessed_and_complete(year, first_day, last_day, session)]

    # processing games needs to go to a higher level so we can know how to process a given game
    def process_games_for_days(self, year, first_day, last_day, session=None):
        commit = session is None
        session = self.get_session(session)

        games_to_process = self.repo.get_by_unprocessed_and_complete(year, first_day, last_day, session)

        for game in games_to_process:
            home_record = self.record_repo.get_by_team_and_year(game.home_team.oid, year, session)
            away_record = self.record_repo.get_by_team_and_year(game.away_team.oid, year, session)

            home_record.process_game(game.home_score, game.away_score)
            away_record.process_game(game.away_score, game.home_score)

            game.processed = True

        self.commit(session, commit)

    def process_games_before(self, year, before_this_day, session=None):
        raise NotImplementedError

    def get_incomplete_games_by_year_count(self, year, session=None):
        session = self.get_session(session)
        repo = GameRepository()
        return repo.get_incomplete_or_unprocessed_games_by_year_count(year, session)
