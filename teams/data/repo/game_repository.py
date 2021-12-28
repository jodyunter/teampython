from sqlalchemy import select, and_
from sqlalchemy.sql import or_

from teams.data.dto.dto_game import GameDTO
from teams.data.repo.repository import Repository


class GameRepository(Repository):

    def get_type(self):
        return GameDTO

    def get_by_unprocessed_and_complete(self, year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.processed == False, GameDTO.complete == True,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    def get_games_by_day(self, year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    def get_incomplete_games_by_day(self, year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.complete == False,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    def get_incomplete_or_unprocessed_games_by_day(self, year, first_day, last_day, session):
        return session.query(GameDTO).filter(GameDTO.complete == False or GameDTO.processed == False,
                                             GameDTO.day >= first_day,
                                             GameDTO.day <= last_day,
                                             GameDTO.year == year)

    def get_incomplete_or_unprocessed_games_by_year_count(self, year, session):
        return session.query(GameDTO).filter(GameDTO.complete == False or GameDTO.processed == False,
                                             GameDTO.year == year).count()

    def get_list_days_teams_play_on(self, year, starting_day, ending_day, game, session):
        home_id = game.home_team.oid
        away_id = game.away_team.oid

        stmnt = select(GameDTO.day).where(and_(
            GameDTO.year == year,
            GameDTO.day >= starting_day,
            GameDTO.day <= ending_day,
            or_(
                GameDTO.home_team_id == home_id,
                GameDTO.home_team_id == away_id,
                GameDTO.away_team_id == home_id,
                GameDTO.away_team_id == away_id
            )))

        result = session.execute(stmnt).fetchall()

        return [a[0] for a in result]



