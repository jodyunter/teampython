from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.base_repository import BaseRepository


class GameRepository(BaseRepository):
    def get_type(self):
        return GameDTO

    @staticmethod
    def add(game, session):
        game_dto = GameDTO(game)
        session.add(game_dto)
        pass

    def get_by_unprocessed_and_complete(self, year, first_day, last_day, session):
        my_type = self.get_type()
        return session.query(my_type).filter(my_type.processed == False, my_type.complete == True,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    def get_games_by_day(self, year, first_day, last_day, session):
        my_type = self.get_type()
        return session.query(my_type).filter(my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    def get_incomplete_games_by_day(self, year, first_day, last_day, session):
        my_type = self.get_type()
        return session.query(my_type).filter(my_type.complete == False,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    def get_incomplete_or_unprocessed_games_by_day(self, year, first_day, last_day, session):
        my_type = self.get_type()
        return session.query(my_type).filter(my_type.complete == False or my_type.processed == False,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    def get_incomplete_or_unprocessed_games_by_year_count(self, year, session):
        my_type = self.get_type()
        return session.query(my_type).filter(my_type.complete == False or my_type.processed == False,
                                             my_type.year == year).count()
