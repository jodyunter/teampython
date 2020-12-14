from teams.data.repo.configuration_repository import ConfigurationRepository
from teams.domain.gamedata import GameData
from teams.services.base_service import BaseService
from teams.services.game_service import GameService
from teams.services.view_models.controller_view_models import GameDataViewModel


class AppService(BaseService):
    repo = ConfigurationRepository()
    game_service = GameService()

    def get_current_data(self):
        session = self.get_session()
        game_data = self.repo.get_current_data(session)
        return GameDataViewModel(game_data.current_year, game_data.current_day)

    def setup_data(self, year, day):
        session = self.get_session()
        game_data = GameData(year, day)
        self.repo.add(game_data, session)

    def change_day(self, new_day, session):
        commit = self.should_commit(session)

        game_data = self.repo.get_current_data(session)
        game_data.current_day = new_day

        self.commit(commit, session)

    def change_year(self, new_year, session):
        commit = self.should_commit(session)

        game_data = self.repo.get_current_data(session)
        game_data.current_year = new_year

        self.commit(commit, session)

    def go_to_next_day(self, session):
        commit = self.should_commit(session)

        game_data = self.repo.get_current_data(session)
        yes = self.is_day_complete(game_data.current_year, game_data.current_day, game_data.current_day, session)

        if yes:
            self.change_day(game_data.current_day + 1, session)

        self.commit(commit, session)

    def is_day_complete(self, year, first_day, last_day, session):
        commit = self.should_commit(session)
        day_is_complete = False

        games_unprocessed = self.game_service.get_complete_and_unprocessed_games_for_days(year, first_day, last_day, session)

        if len(games_unprocessed) == 0:
            day_is_complete = True

        self.commit(commit, session)

        return day_is_complete

    def is_year_complete(self):
        raise NotImplementedError

    def play_and_process_games_for_current_day(self):
        raise NotImplementedError
