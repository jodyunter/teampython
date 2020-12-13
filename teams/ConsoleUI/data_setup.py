# create teams
from teams.services.game_service import GameRulesService
from teams.services.team_service import TeamService

team_name_list = ["Toronto", "Vancouver", "Ottawa", "Montreal", "Quebec City", "Winnipeg",
                  "Calgary", "Edmonton", "Saskatoon", "Victoria", "Halifax", "Regina", "Hamilton",
                  "London", "St John's"]
# team_name_list = ["Toronto", "Vancouver", "Ottawa"]


def setup():
    team_service = TeamService()
    [team_service.create(n, 0) for n in team_name_list]
    game_rules_service = GameRulesService()
    game_rules_service.create("Season", True)

