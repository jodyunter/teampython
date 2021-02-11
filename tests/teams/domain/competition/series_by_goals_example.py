import uuid
import random

from teams.domain.competition import Competition, CompetitionTeam, PlayoffSubCompetition
from teams.domain.series import SeriesByGoals
from teams.domain.game import GameRules
from teams.domain.series_rules import SeriesByGoalsRules
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper

home_team = Team("Team 1", 5, True, IDHelper.get_new_id())
away_team = Team("Team 2", 5, True, IDHelper.get_new_id())

competition = Competition("My Comp", 1, None, True, True, False, False, IDHelper.get_new_id())
sub_competition = PlayoffSubCompetition("Playoff A", None, competition, True, True, False, False, IDHelper.get_new_id())

home_competition_team = CompetitionTeam(competition, home_team, IDHelper.get_new_id())
away_competition_team = CompetitionTeam(competition, away_team, IDHelper.get_new_id())

game_rules = GameRules("Playoff", True, IDHelper.get_new_id())
last_game_rules = GameRules("Last Game", False, IDHelper.get_new_id())

series_rules = SeriesByGoalsRules("My Rules", 2, game_rules, last_game_rules, IDHelper.get_new_id())


series = SeriesByGoals(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                       0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                       True, False,
                       IDHelper.get_new_id())

games = []

while not series.is_complete():
    complete_games = [g for g in games if g.complete and g.processed]
    incomplete_games = [g for g in games if not g.complete]

    games.extend(series.get_new_games(len(complete_games), len(incomplete_games)))

    r = random
    for game in games:
        game.play(r)

        series.process_game(game)

        print(series.name)
        print(f'{game.game_number}. {game.home_team.name} : {game.home_score} - {game.away_score} : {game.away_team.name}')
        print(series.home_team.name + " : " + str(series.home_goals))
        print(series.away_team.name + " : " + str(series.away_goals))


print("Winner is: " + series.get_winner().name)
