from teams.data.dto.dto_game_data import GameDataDTO
from teams.data.repo.game_data_repository import GameDataRepository
from teams.domain.gamedata import GameData
from teams.services.base_service import BaseService
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from teams.services.view_models.app_view_models import GameDataViewModel


class AppService(BaseService):

    def __init__(self):
        pass

    def get_current_data(self, session=None):
        session = self.get_session(session)
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        return GameDataViewModel(game_data.current_year, game_data.current_day,
                                 game_data.is_year_setup, game_data.is_year_finished)

    def setup_data(self, year, day, setup, finished, session=None):
        commit = session is None
        session = self.get_session(session)
        game_data = GameData("game_data", year, day, setup, finished)
        GameDataRepository.add(game_data, GameDataDTO, session)
        self.commit(session, commit)

    def change_day(self, new_day, session=None):
        commit = session is None
        session = self.get_session(session)
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        game_data.current_day = new_day
        self.commit(session, commit)

    def change_year(self, new_year, session=None):
        commit = self.get_session(session)
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        game_data.current_year = new_year
        game_data.current_day = 1
        game_data.is_year_finished = False
        game_data.is_year_setup = False

        # repo.update(game_data, session)

        self.commit(session, commit)

    def go_to_next_day(self, session=None):
        commit = session is None
        session = self.get_session(session)
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        yes = self.is_day_complete(session)

        if yes:
            self.change_day(game_data.current_day + 1, session)

        self.commit(session, commit)

    def go_to_next_year(self, session=None):
        commit = session is None
        session = self.get_session(session)
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)

        yes = self.is_year_complete()

        if yes:
            self.change_year(game_data.current_year + 1, session)

        self.commit(session, commit)

    def is_day_complete(self, session=None):
        session = self.get_session(session)
        day_is_complete = False
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        game_service = GameService()
        games_unprocessed = game_service.get_incomplete_games_for_days(game_data.current_year,
                                                                       game_data.current_day,
                                                                       game_data.current_day, session)

        if len(games_unprocessed) == 0:
            day_is_complete = True

        return day_is_complete

    def is_year_complete(self, session=None):
        session = self.get_session(session)
        game_service = GameService()
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)
        if game_data.is_year_finished:
            return True
        else:
            return game_service.get_incomplete_games_by_year_count(game_data.current_year,
                                                                   session) <= 0

    def play_and_process_games_for_current_day(self, r, session=None):
        commit = session is None
        session = self.get_session(session)

        # get games for current day and play and process if needed
        game_service = GameService()
        repo = GameDataRepository()
        game_data = repo.get_current_data(session)

        if not self.is_day_complete(session):
            game_service.play_games_for_days(game_data.current_year, game_data.current_day, game_data.current_day, r,
                                             session)
            game_service.process_games_for_days(game_data.current_year, game_data.current_day, game_data.current_day,
                                                session)

        record_service = RecordService()
        record_service.update_rank(game_data.current_year, session)

        # check if day complete and processed
        if self.is_day_complete(session):
            self.go_to_next_day(session)

        # increment day
        if self.is_year_complete(session):
            game_data.is_year_finished = True

        self.commit(session, commit)

    def setup_year(self, rules, rounds, home_and_away, session=None):
        commit = session is None
        session = self.get_session(session)
        team_service = TeamService()
        record_service = RecordService()
        game_service = GameService()
        repo = GameDataRepository()

        game_data = repo.get_current_data(session)
        if not game_data.is_year_setup:
            team_list = team_service.get_active_teams(session)
            record_service.add(team_list, game_data.current_year, session)
            game_service.create_games(team_list, game_data.current_year, game_data.current_day, rules,
                                      rounds, home_and_away, session)
            game_data.is_year_setup = True

        self.commit(session, commit)
