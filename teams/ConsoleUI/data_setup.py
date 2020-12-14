# create teams
from teams.services.app_service import AppService
from teams.services.game_service import GameRulesService
from teams.services.team_service import TeamService

team_name_list = ["Toronto", "Vancouver", "Ottawa", "Montreal", "Quebec City", "Winnipeg",
                  "Calgary", "Edmonton", "Victoria"]
# team_name_list = ["Toronto", "Vancouver", "Ottawa"]


def setup():
    team_service = TeamService()
    [team_service.create(n, 0) for n in team_name_list]
    game_rules_service = GameRulesService()
    game_rules_service.create("Season", True)
    app_service = AppService()
    app_service.setup_data(1, 1)

