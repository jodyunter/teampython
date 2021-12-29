# create teams
from teams.services.app_service import AppService
from teams.services.game_service import GameRulesService
from teams.services.team_service import TeamService

team_name_list = ["Toronto", "Montreal", "Ottawa"]


# team_name_list = ["Toronto", "Vancouver", "Ottawa"]


def setup():
    # team_service = TeamService()
    # [team_service.create(n, 0) for n in team_name_list]
    game_rules_service = GameRulesService()
    game_rules_service.create("Season", True)
    game_rules_service.create("Playoff", False)
    app_service = AppService()
    app_service.setup_data(0, 0, True, True)


def add_new_teams():
    app_service = AppService()
    team_service = TeamService()
    game_data = app_service.get_current_data()
    teams_to_add = get_next_teams(str(game_data.current_year))
    for t in teams_to_add:
        team_service.create(t, 0, True)


def get_next_teams(year_string):
    return {
        "0": ["Montreal", "Toronto", "Ottawa", "Calgary", "Edmonton", "Vancouver", "Winnipeg", "Quebec City", "Halifax", "Victoria", "Saskatoon"],
        "8": ["Detroit"],
        "9": ["Pittsburgh"],
        "10": ["New York"],
        "11": ["Chicago"],
        "12": ["Philadelphia"],
        "13": ["Buffalo"],
        "14": ["Seattle"],
        "15": ["Colorado"],
        "16": ["Boston"],
        "17": ["Minnesota"]
    }.get(year_string, [])

