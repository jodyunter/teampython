import random

from teams.domain.competition import Competition, CompetitionTeam
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals
from teams.domain.series_rules import SeriesByGoalsRules
from teams.domain.sub_competition import PlayoffSubCompetition
from teams.domain.team import Team

home_team = Team("Team 1", 5, True)
away_team = Team("Team 2", 5, True)

competition = Competition("My Comp", 1, None, None, True, True, False, False)
sub_competition = PlayoffSubCompetition("Playoff A", None, competition, 1, 1, True, True, False, False)

home_competition_team = CompetitionTeam(competition, home_team)
away_competition_team = CompetitionTeam(competition, away_team)

game_rules = GameRules("Playoff", True)
last_game_rules = GameRules("Last Game", False)

series_rules = SeriesByGoalsRules("My Rules", 2, game_rules, last_game_rules, None)


series = SeriesByGoals(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                       0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                       True, False)

games = []

print(series.name)
while not series.is_complete():
    complete_games = [g for g in games if g.complete and g.processed]
    incomplete_games = [g for g in games if not g.complete]

    games.extend(series.get_new_games(len(complete_games), len(incomplete_games)))

    r = random
    for game in games:
        game.play(r)
        if not game.processed:
            series.process_game(game)
            print(f'{game.game_number}. {game.home_team.name} : {game.home_score} - {game.away_score} : {game.away_team.name}')

    print(series.home_team.name + " : " + str(series.home_goals))
    print(series.away_team.name + " : " + str(series.away_goals))

print("Winner is: " + series.get_winner().name)
