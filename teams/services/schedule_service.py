from teams.services.base_service import BaseService


class ScheduleService(BaseService):

    @staticmethod
    def add_game_to_schedule(game, starting_day):
        # using queries, find the first day on or after the starting day, where the two teams do not play
        pass
