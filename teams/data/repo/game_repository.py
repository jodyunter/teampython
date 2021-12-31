from sqlalchemy import select, and_
from sqlalchemy.sql import or_

from teams.data.dto.dto_competition_game import CompetitionGameDTO
from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_series_games import SeriesGameDTO
from teams.data.repo.repository import Repository


class GameRepository(Repository):

    def get_type(self):
        return GameDTO

    def get_by_unprocessed_and_complete(self, year, first_day, last_day, session):
        dto_type = self.get_type()
        return session.query(dto_type).filter(dto_type.processed == False, dto_type.complete == True,
                                              dto_type.day >= first_day,
                                              dto_type.day <= last_day,
                                              dto_type.year == year)

    def get_games_by_day(self, year, first_day, last_day, session):
        dto_type = self.get_type()
        return session.query(dto_type).filter(dto_type.day >= first_day,
                                              dto_type.day <= last_day,
                                              dto_type.year == year)

    def get_incomplete_games_by_day(self, year, first_day, last_day, session):
        dto_type = self.get_type()
        return session.query(dto_type).filter(dto_type.complete == False,
                                              dto_type.day >= first_day,
                                              dto_type.day <= last_day,
                                              dto_type.year == year)

    def get_incomplete_or_unprocessed_games_by_day(self, year, first_day, last_day, session):
        dto_type = self.get_type()
        return session.query(dto_type).filter(dto_type.complete == False or dto_type.processed == False,
                                              dto_type.day >= first_day,
                                              dto_type.day <= last_day,
                                              dto_type.year == year)

    def get_incomplete_or_unprocessed_games_by_year_count(self, year, session):
        dto_type = self.get_type()
        return session.query(dto_type).filter(dto_type.complete == False or dto_type.processed == False,
                                              dto_type.year == year).count()

    def get_list_days_team_play_on_stmt(self, year, starting_day, ending_day, game):
        dto_type = self.get_type()

        home_id = game.home_team.oid
        away_id = game.away_team.oid

        stmt = select(dto_type.day).where(and_(
            dto_type.year == year,
            dto_type.day >= starting_day,
            dto_type.day <= ending_day,
            or_(
                dto_type.home_team_id == home_id,
                dto_type.home_team_id == away_id,
                dto_type.away_team_id == home_id,
                dto_type.away_team_id == away_id
            )))

        return stmt

    def get_list_days_teams_play_on(self, year, starting_day, ending_day, game, session):
        stmt = self.get_list_days_team_play_on_stmt(year, starting_day, ending_day, game)

        result = session.execute(stmt).fetchall()

        return [a[0] for a in result]


# todo: can we get subclasses of GameDTO when we use GameDTO or will we need multiple queries to process a full day?
class CompetitionGameRepository(GameRepository):

    def get_type(self):
        return CompetitionGameDTO

    def get_by_competition_and_year(self, session):
        # can we add this to the above queries?
        pass


class SeriesGameRepository(CompetitionGameRepository):

    def get_type(self):
        return SeriesGameDTO

    def get_by_series(self):
        # can we add a year or anything else to the above queries?
        pass
