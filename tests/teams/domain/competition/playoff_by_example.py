import random

from teams.ConsoleUI.views.game_view import GameView
from teams.domain.competition import PlayoffSubCompetition, CompetitionTeam, Competition
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByGoalsRules, SeriesByWinsRules
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper
from teams.services.game_service import GameService

competition = Competition("My Comp", 25, None, True, True, False, False, IDHelper.get_new_id())

playoff = PlayoffSubCompetition("My Playoff", None, competition, True, True, False, False, IDHelper.get_new_id())
competition.sub_competitions = [playoff]

tie_game_rules = GameRules("Can Tie", True, IDHelper.get_new_id())
not_tie_game_rules = GameRules("Not Tie", False, IDHelper.get_new_id())

series_goals_rules = SeriesByGoalsRules("By Goals", 2, tie_game_rules, not_tie_game_rules, IDHelper.get_new_id())
series_wins_rules = SeriesByWinsRules("By Wins", 2, not_tie_game_rules, None, IDHelper.get_new_id())

team_list = [
    Team("Team 1", 5, True, IDHelper.get_new_id()),
    Team("Team 2", 5, True, IDHelper.get_new_id()),
    Team("Team 3", 5, True, IDHelper.get_new_id()),
    Team("Team 4", 5, True, IDHelper.get_new_id()),
    Team("Team 5", 5, True, IDHelper.get_new_id()),
    Team("Team 6", 5, True, IDHelper.get_new_id())
]

competition_team_list = [
    CompetitionTeam(competition, team_list[0], IDHelper.get_new_id()),
    CompetitionTeam(competition, team_list[1], IDHelper.get_new_id()),
    CompetitionTeam(competition, team_list[2], IDHelper.get_new_id()),
    CompetitionTeam(competition, team_list[3], IDHelper.get_new_id()),
    CompetitionTeam(competition, team_list[4], IDHelper.get_new_id()),
    CompetitionTeam(competition, team_list[5], IDHelper.get_new_id())
]

series1 = SeriesByGoals(playoff, "Series 1", 1, competition_team_list[0], competition_team_list[1], 0, 0, 0,
                        series_goals_rules, None, None, None, None, None, None, None, None, True, False,
                        IDHelper.get_new_id())

series2 = SeriesByGoals(playoff, "Series 2", 1, competition_team_list[2], competition_team_list[3], 0, 0, 0,
                        series_goals_rules, None, None, None, None, None, None, None, None, True, False,
                        IDHelper.get_new_id())

series3 = SeriesByWins(playoff, "Series 3", 1, competition_team_list[4], competition_team_list[5], 0, 0,
                       series_wins_rules, None, None, None, None, None, None, None, None,
                       True, False, IDHelper.get_new_id())

playoff.series = [series1, series2, series3]

COMPLETE = "Complete Games"
INCOMPLETE = "Incomplete Games"
game_status_map = playoff.create_series_map([])

r = random

games = []
current_round = 1
loop = 0

while not playoff.is_complete():
    print(loop)
    new_games = playoff.create_new_games(game_status_map[COMPLETE], game_status_map[INCOMPLETE])
    games.extend(new_games)
    for g in new_games:
        g.play(r)
        model = GameService.game_to_vm(g)
        playoff.process_game(g)
        print(GameView.get_basic_view(model))

    game_status_map = playoff.create_series_map(games)

    loop += 1

