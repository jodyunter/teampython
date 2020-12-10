from teams.services.team_service import TeamService
from teams.services.view_models.game_view_models import GameViewModel


class GameService:
    team_service = TeamService()

    def play_game(self, home_team_id, away_team_id, year, day, rules):
        home_team = self.team_service.get_by_id(home_team_id)
        away_team = self.team_service.get_by_id(away_team_id)

        return GameViewModel(year, day, home_team.name, home_team_id,
                             away_team.name, away_team_id,
                             0, 0, "Complete")
