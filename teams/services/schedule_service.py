from teams.data.repo.game_repository import GameRepository
from teams.services.base_service import BaseService


class ScheduleService(BaseService):
    game_repo = GameRepository()

    def get_repo(self):
        return self.game_repo

    # this is using a domain object in the game
    def add_game_to_schedule(self, game_view_model, starting_day, ending_day, session=None):
        commit = session is None
        session = self.get_session(session)

        if ending_day is None:
            ending_day = 99999
            
        days = self.get_repo().get_invalid_schedule_days(game_view_model.year, starting_day, ending_day,
                                                         [game_view_model.home_id,
                                                          game_view_model.away_id], session)

        days.sort()

        added = False
        day = starting_day
        while not added:
            if day not in days:
                game_view_model.day = day
                added = True
            else:
                day += 1

        self.get_repo().add(game_view_model, session)

        self.commit(session, commit)
