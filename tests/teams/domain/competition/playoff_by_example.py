import random
from teams.ConsoleUI.views.playoff_views import SeriesView
from teams.domain.competition import CompetitionTeam, Competition, CompetitionGroup
from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByGoalsRules, SeriesByWinsRules
from teams.domain.sub_competition import PlayoffSubCompetition
from teams.domain.team import Team
from teams.services.game_service import GameService
from teams.services.view_models.playoff_view_models import SeriesViewModel
from teams.services.view_models.team_view_models import TeamViewModel

competition = Competition("My Comp", 25, None, True, True, False, False)

playoff = PlayoffSubCompetition("My Playoff", None, competition, 1, 1, True, True, False, False)
competition.sub_competitions = [playoff]

league = CompetitionGroup("League", None, None, [], CompetitionGroupConfiguration.RANKING_TYPE)
eastern = CompetitionGroup("Eastern", league, None, [], CompetitionGroupConfiguration.RANKING_TYPE)
western = CompetitionGroup("Western", league, None, [], CompetitionGroupConfiguration.RANKING_TYPE)

groups = [league, eastern, western]

tie_game_rules = GameRules("Can Tie", True)
not_tie_game_rules = GameRules("Not Tie", False)

series_goals2_rules = SeriesByGoalsRules("By Goals 2 games", 2, tie_game_rules, not_tie_game_rules)
series_goals3_rules = SeriesByGoalsRules("By Goals 3 games", 3, tie_game_rules, not_tie_game_rules)
series_wins2_rules = SeriesByWinsRules("By Wins 2 wins", 2, not_tie_game_rules, None)
series_wins4_rules = SeriesByWinsRules("By Wins 4 wins", 4, not_tie_game_rules, None)

team_list = []
competition_team_list = []

league_count = 1
eastern_count = 1
western_count = 1
for i in range(10):
    team = Team("Team " + str(i), 5, True)
    team_list.append(team)
    competition_team_list.append(CompetitionTeam(competition, team))
    league.add_team_to_group(team, league_count)
    league_count += 1
    if i % 2 == 0:
        western.add_team_to_group(team, western_count)
        western_count += 1
    else:
        eastern.add_team_to_group(team, eastern_count)
        eastern_count += 1


series1 = SeriesByGoals(playoff, "Series 1", 1, None, None, 0, 0, 0,
                        series_goals2_rules, league, 1, league, 2, None, None, None, None, False, False)

series2 = SeriesByGoals(playoff, "Series 2", 1, None, None, 0, 0, 0,
                        series_goals2_rules, league, 3, league, 4, None, None, None, None, False, False)

series3 = SeriesByWins(playoff, "Series 3", 1, None, None, 0, 0,
                       series_wins2_rules, league, 5, league, 6, None, None, None, None, False, False)

series4 = SeriesByWins(playoff, "Series 4", 1, None, None, 0, 0,
                       series_wins4_rules, league, 7, league, 8, None, None, None, None, False, False)

series5 = SeriesByWins(playoff, "Series 5", 2, competition_team_list[8], competition_team_list[9], 0, 0,
                       series_wins4_rules, None, None, None, None, None, None, None, None, False, False)

series6 = SeriesByGoals(playoff, "Series 6", 3, competition_team_list[2], competition_team_list[3], 0, 0, 0,
                        series_goals3_rules, None, None, None, None, None, None, None, None, False, False)

playoff.series = [series1, series2, series3, series4]

COMPLETE = "Complete Games"
INCOMPLETE = "Incomplete Games"
game_status_map = playoff.create_series_map([])

r = random

games = []
loop = 0

#  setup first round of playoff
while not playoff.is_complete():
    print(f'Current Round: {playoff.current_round}')
    while not playoff.is_round_complete(playoff.current_round):
        if not playoff.is_round_setup(playoff.current_round):
            playoff.setup_round(playoff.current_round)
        # print(loop)
        new_games = playoff.create_new_games(game_status_map[COMPLETE], game_status_map[INCOMPLETE])
        games.extend(new_games)
        for g in new_games:
            g.play(r)
            model = GameService.game_to_vm(g)
            playoff.process_game(g)
            # print(GameView.get_basic_view(model))
        loop += 1
        game_status_map = playoff.create_series_map(games)

    for s in [ps for ps in playoff.series if ps.series_round == playoff.current_round]:
        home_value = -1
        away_value = -1
        if isinstance(s, SeriesByGoals):
            home_value = s.home_goals
            away_value = s.away_goals
        elif isinstance(s, SeriesByWins):
            home_value = s.home_wins
            away_value = s.away_wins

        view_model = SeriesViewModel(s.name, s.sub_competition.competition.year, s.series_round, None,
                                     TeamViewModel(s.home_team.oid, s.home_team.name, s.home_team.skill, True),
                                     home_value,
                                     TeamViewModel(s.away_team.oid, s.away_team.name, s.away_team.skill, True),
                                     away_value,
                                     "Done")
        print(SeriesView.get_basic_series_view(view_model))
    # post process round and series
    playoff.current_round += 1

# post process the playoff
