import os
import uuid
import random

from teams.domain.competition import Competition, CompetitionTeam, SeriesByGoals, CompetitionGame
from teams.domain.game import GameRules
from teams.domain.series_rules import SeriesByGoalsRules
from teams.domain.team import Team

home_team = Team("Team 1", 5, True, uuid.uuid4())
away_team = Team("Team 2", 5, True, uuid.uuid4())

competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

series_rules = SeriesByGoalsRules("My Rules", 3, None)

series = SeriesByGoals(None, "My Series", 1, home_competition_team, away_competition_team,
                       0, 0, 0, series_rules, None, None, None, None, None, None, None, None, None,
                       True, False,
                       uuid.uuid4())

game_rules = GameRules("Playoff", False, uuid.uuid4())

while not series.is_complete():
    os.system('cls')
    game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 0, 0, False, False,
                           game_rules, uuid.uuid4())

    r = random

    game.play(r)

    series.process_game(game)

    print(series.name)
    print(series.home_team.name + " : " + str(series.home_goals))
    print(series.away_team.name + " : " + str(series.away_goals))


print("Winner is: " + series.get_winner().name)
