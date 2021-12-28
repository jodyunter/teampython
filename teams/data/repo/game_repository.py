from sqlalchemy import func

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

    @staticmethod
    def get_first_day_for_game(year, starting_day, game, session):
        home_id = game.home_team.oid
        away_id = game.away_team.oid

        result = session.query(func.min(GameDTO.day))\
            .filter(GameDTO.year == year,
                    GameDTO.day >= starting_day,
                    GameDTO.home_team_id != home_id,
                    GameDTO.home_team_id != away_id,
                    GameDTO.away_team_id != home_id,
                    GameDTO.away_team_id != away_id).scalar()

        return result

