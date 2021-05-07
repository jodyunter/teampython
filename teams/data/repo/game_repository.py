from teams.data.dto.dto_game import GameDTO
from teams.data.repo.repository import Repository


class GameRepository(Repository):

    @staticmethod
    def get_by_unprocessed_and_complete(year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.processed == False, GameDTO.complete == True,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    @staticmethod
    def get_games_by_day(year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    @staticmethod
    def get_incomplete_games_by_day(year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.complete == False,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    @staticmethod
    def get_incomplete_or_unprocessed_games_by_day(year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.complete == False or GameDTO.processed == False,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    @staticmethod
    def get_incomplete_or_unprocessed_games_by_year_count(year, session):
        return session.query(GameDTO).filter(GameDTO.complete == False or GameDTO.processed == False,
                                             GameDTO.year == year).count()
