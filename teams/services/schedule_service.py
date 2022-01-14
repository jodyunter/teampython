from teams.data.repo.game_repository import GameRepository
from teams.services.base_service import BaseService


class ScheduleService(BaseService):
    game_repo = GameRepository()

    def get_repo(self):
        return self.game_repo

    def add_game_to_schedule(self, game, starting_day, session=None):
        commit = session is None
        session = self.get_session(session)
        ending_day = 99999
        days = self.get_repo().get_list_days_teams_play_on(game.year, starting_day, ending_day, game, session)

        days.sort()

        added = False
        day = starting_day
        while not added:
            if not day in days:
                game.day = day
                added = True
            else:
                day += 1

        self.get_repo().add(game)

        self.commit(session, commit)
