from teams.data.repo.game_repository import GameRepository
from teams.services.base_service import BaseService


class ScheduleService(BaseService):
    game_repo = GameRepository()

    def get_repo(self):
        return self.game_repo

    # this is using a domain object in the game
    def add_game_to_schedule(self, year, game_view_model, starting_day, ending_day, session=None):
        commit = session is None
        session = self.get_session(session)

        self.add_games_as_day(year, [game_view_model], starting_day, ending_day, session)

        self.commit(session, commit)

    def add_games_as_day(self, year, game_view_model_list, starting_day, ending_day, session=None):
        commit = session is None
        session = self.get_session(session)

        team_id_list = [game_vm.home_id for game_vm in game_view_model_list]
        team_id_list.append([game_vm.away_id for game_vm in game_view_model_list])

        if ending_day is None:
            ending_day = 99999

        days = self.get_repo().get_invalid_schedule_days(year, starting_day, ending_day,
                                                         team_id_list, session)

        days.sort()

        added = False
        day = starting_day
        while not added:
            if day not in days:
                for game_vm in game_view_model_list:
                    game_vm.day = day
                added = True
            else:
                day += 1

        for game_vm in game_view_model_list:
            self.get_repo().add(game_vm, session)

        self.commit(session, commit)
