# create teams
from teams.services.team_service import TeamService

team_name_list = ["Toronto", "Vancouver", "Ottawa", "Montreal", "Quebec City", "Winnipeg", "Calgary", "Edmonton",
                  "Vancouver"]


def setup():
    team_service = TeamService()
    [team_service.create(n, 0) for n in team_name_list]
