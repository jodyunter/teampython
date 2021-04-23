from teams.data.dto.dto_game import GameDTO
from teams.data.repo.repository import Repository


class GameRepository(Repository):

    @staticmethod
    def get_by_unprocessed_and_complete( year, first_day, last_day, session):
        my_type = GameDTO
        return session.query(my_type).filter(my_type.processed == False, my_type.complete == True,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    @staticmethod
    def get_games_by_day(year, first_day, last_day, session):
        my_type = GameDTO
        return session.query(my_type).filter(my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    @staticmethod
    def get_incomplete_games_by_day(year, first_day, last_day, session):
        my_type = GameDTO
        return session.query(my_type).filter(my_type.complete == False,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    @staticmethod
    def get_incomplete_or_unprocessed_games_by_day(year, first_day, last_day, session):
        my_type = GameDTO
        return session.query(my_type).filter(my_type.complete == False or my_type.processed == False,
                                             my_type.day >= first_day,
                                             my_type.day <= last_day,
                                             my_type.year == year)

    @staticmethod
    def get_incomplete_or_unprocessed_games_by_year_count(year, session):
        my_type = GameDTO
        return session.query(my_type).filter(my_type.complete == False or my_type.processed == False,
                                             my_type.year == year).count()
