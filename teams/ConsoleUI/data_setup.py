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
    app_service = AppService()
    app_service.setup_data(0, 0, True, True)


def add_new_teams():
    app_service = AppService()
    team_service = TeamService()
    game_data = app_service.get_current_data()
    teams_to_add = get_next_teams(str(game_data.current_year))
    for t in teams_to_add:
        team_service.create(t, 0)


def get_next_teams(year_string):
    return {
        "0": ["Montreal", "Toronto", "Ottawa"],
        "5": ["Detroit"],
        "10": ["Boston"],
        "15": ["New York"],
        "20": ["Vancouver"],
        "25": ["Calgary"],
        "30": ["Edmonton"],
        "35": ["Minnesota"],
        "40": ["Chicago"],
        "45": ["Colorado"],
        "50": ["Seattle"],
        "55": ["Pittsburgh"],
        "65": ["Philadelphia"],
        "65": ["Winnipeg"],
        "70": ["New Jersey"],
        "75": ["Los Angelas"],
        "80": ["Quebec City"],
        "85": ["Nashville"],
        "90": ["Columbus"],
        "95": ["Washington"],
        "100": ["Las Vegas"],
        "105": ["San Jose"],
        "110": ["Buffalo"],
        "115": ["Atlanta"],
        "120": ["Tampa Bay"],
        "125": ["Florida"],
        "130": ["Hamilton"],
        "135": ["London"],
        "140": ["Anaheim"],
        "145": ["Dallas"]
    }.get(year_string, [])
