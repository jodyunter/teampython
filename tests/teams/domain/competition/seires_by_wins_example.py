import random

from teams.domain.competition import Competition, CompetitionTeam
from teams.domain.series import SeriesByWins
from teams.domain.game import GameRules
from teams.domain.series_rules import SeriesByWinsRules
from teams.domain.sub_competition import PlayoffSubCompetition
from teams.domain.team import Team

home_team = Team("Team 1", 5, True)
away_team = Team("Team 2", 5, True)

competition = Competition("My Comp", 1, None, None, True, True, False, False)
sub_competition = PlayoffSubCompetition("Playoff A", None, competition, 1, 1, True, True, False, False)

home_competition_team = CompetitionTeam(competition, home_team)
away_competition_team = CompetitionTeam(competition, away_team)

game_rules = GameRules("Playoff", False)

series_rules = SeriesByWinsRules("My Rules", 4, game_rules, [0, 0, 1, 1, 0, 1, 0])

series = SeriesByWins(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                      0, 0, series_rules, None, None, None, None, None, None, None, None,
                      True, False)

games = []

print(series.name)
while not series.is_complete():
    complete_games = [g for g in games if g.complete and g.processed]
    incomplete_games = [g for g in games if not g.complete]

    games.extend(series.get_new_games(len(complete_games), len(incomplete_games)))

    r = random
    for game in games:
        if not game.complete:
            game.play(r)
            series.process_game(game)
            print(f'{game.game_number}. {game.home_team.name} : {game.home_score} - {game.away_score} : {game.away_team.name}')

print(f'{series.home_team.name} : {series.home_wins} - {series.away_wins} : {series.away_team.name}')
print("Winner is: " + series.get_winner().name)
