from random import randint

from teams.domain.game import Game
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from teams.services.view_models.game_view_models import GameViewModel


class GameService:
    team_service = TeamService()
    record_service = RecordService()

    def play_game(self, home_team_id, away_team_id, year, day, rules):
        home_team = self.team_service.get_by_id(home_team_id)
        away_team = self.team_service.get_by_id(away_team_id)

        game = Game()
        return GameViewModel(year, day, home_team.name, home_team_id,
                             away_team.name, away_team_id,
                             home_score, away_score, "Complete")

    def process_game(self, year, home_team_id, home_score, away_team_id, away_score):
        home_record = self.record_service.get_by_team_and_year(home_team_id, year)
        away_record = self.record_service.get_by_team_and_year(away_team_id, year)

        home_record.process_game(home_score, away_score)
        away_record.process_game(away_score, home_score)

        self.record_service.update_records([home_record, away_record])
