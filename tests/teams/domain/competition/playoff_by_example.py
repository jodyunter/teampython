import random

from teams.ConsoleUI.views.game_view import GameDayView
from teams.ConsoleUI.views.playoff_views import SeriesView
from teams.domain.competition import CompetitionTeam, Competition, CompetitionGroup
from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByGoalsRules, SeriesByWinsRules
from teams.domain.sub_competition import PlayoffSubCompetition
from teams.domain.team import Team
from teams.services.game_service import GameService
from teams.services.view_models.playoff_view_models import SeriesViewModel
from teams.services.view_models.team_view_models import TeamViewModel


def add_teams_to_group(teams, group):
    count = 1
    for t in teams:
        group.add_team_to_group(t, count)
        count += 1


competition = Competition("My Comp", 25, None, True, True, False, False)

playoff = PlayoffSubCompetition("My Playoff", None, competition, 1, 1, True, True, False, False)
competition.sub_competitions = [playoff]

league = CompetitionGroup("League", None, None, [], CompetitionGroupConfiguration.RANKING_TYPE)
eastern = CompetitionGroup("Eastern", league, None, [], CompetitionGroupConfiguration.RANKING_TYPE)
western = CompetitionGroup("Western", league, None, [], CompetitionGroupConfiguration.RANKING_TYPE)

r1_winners = CompetitionGroup("R1 Winners", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r1_losers = CompetitionGroup("R1 Losers", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r2_winners = CompetitionGroup("R2 Winners", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r3_winners = CompetitionGroup("R3 Winners", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r2_losers = CompetitionGroup("R2 Winners", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r1_western = CompetitionGroup("R1 Western", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
r1_eastern = CompetitionGroup("R1 Eastern", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)

champion = CompetitionGroup("Champion", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
runner_up = CompetitionGroup("Runner-up", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)

groups = [league, eastern, western, r1_winners, r1_losers, r2_winners, r2_losers, champion, runner_up, r1_western,
          r1_eastern]

tie_game_rules = GameRules("Can Tie", True)
not_tie_game_rules = GameRules("Not Tie", False)

series_goals2_rules = SeriesByGoalsRules("By Goals 2 games", 2, tie_game_rules, not_tie_game_rules, None)
series_goals3_rules = SeriesByGoalsRules("By Goals 3 games", 3, tie_game_rules, not_tie_game_rules, None)
series_wins2_rules = SeriesByWinsRules("By Wins 2 wins", 2, not_tie_game_rules, None)
series_wins4_rules = SeriesByWinsRules("By Wins 4 wins", 4, not_tie_game_rules, None)

team_list = []
competition_team_list = []

toronto = CompetitionTeam(competition, Team("Toronto", 5, True))
montreal = CompetitionTeam(competition, Team("Montreal", 5, True))
ottawa = CompetitionTeam(competition, Team("Ottawa", 5, True))
quebec_city = CompetitionTeam(competition, Team("Quebec City", 5, True))
calgary = CompetitionTeam(competition, Team("Calgary", 5, True))
edmonton = CompetitionTeam(competition, Team("Edmonton", 5, True))
vancouver = CompetitionTeam(competition, Team("Vancouver", 5, True))
winnipeg = CompetitionTeam(competition, Team("Winnipeg", 5, True))
victoria = CompetitionTeam(competition, Team("Victoria", 5, True))
saskatoon = CompetitionTeam(competition, Team("Saskatoon", 5, True))
hamilton = CompetitionTeam(competition, Team("Hamilton", 5, True))
halifax = CompetitionTeam(competition, Team("Halifax", 5, True))

league_teams = [toronto, calgary, edmonton, montreal, ottawa, vancouver, winnipeg, quebec_city, victoria, saskatoon,
                hamilton, halifax]
eastern_teams = [toronto, montreal, ottawa, quebec_city, hamilton, halifax]
western_teams = [calgary, edmonton, vancouver, winnipeg, victoria, saskatoon]
r = random
r.shuffle(league_teams)
r.shuffle(eastern_teams)
r.shuffle(western_teams)

add_teams_to_group(league_teams, league)
add_teams_to_group(eastern_teams, eastern)
add_teams_to_group(western_teams, western)

series1 = SeriesByWins(playoff, "Series 1", 1, None, None, 0, 0, series_wins4_rules,
                       eastern, 3, eastern, 6, r1_eastern, league, None, None,
                       False, False)

series2 = SeriesByWins(playoff, "Series 2", 1, None, None, 0, 0, series_wins4_rules,
                       eastern, 4, eastern, 5, r1_eastern, league, None, None,
                       False, False)

series3 = SeriesByWins(playoff, "Series 3", 1, None, None, 0, 0, series_wins4_rules,
                       western, 3, western, 6, r1_western, league, None, None,
                       False, False)

series4 = SeriesByWins(playoff, "Series 4", 1, None, None, 0, 0, series_wins4_rules,
                       western, 4, western, 5, r1_western, league, None, None,
                       False, False)

series5 = SeriesByWins(playoff, "Series 5", 2, None, None, 0, 0, series_wins4_rules,
                       eastern, 1, r1_eastern, 2, r2_winners, league, None, None,
                       False, False)

series6 = SeriesByWins(playoff, "Series 6", 2, None, None, 0, 0, series_wins4_rules,
                       eastern, 2, r1_eastern, 1, r2_winners, league, None, None,
                       False, False)

series7 = SeriesByWins(playoff, "Series 7", 2, None, None, 0, 0, series_wins4_rules,
                       western, 1, r1_western, 2, r2_winners, league, None, None,
                       False, False)

series8 = SeriesByWins(playoff, "Series 8", 2, None, None, 0, 0, series_wins4_rules,
                       western, 2, r1_western, 1, r2_winners, league, None, None,
                       False, False)

series9 = SeriesByWins(playoff, "Series 9", 3, None, None, 0, 0, series_wins4_rules,
                       r2_winners, 1, r2_winners, 4, r3_winners, league, None, None,
                       False, False)

series10 = SeriesByWins(playoff, "Series 10", 3, None, None, 0, 0, series_wins4_rules,
                        r2_winners, 2, r2_winners, 3, r3_winners, league, None, None,
                        False, False)

series11 = SeriesByWins(playoff, "Series 11", 4, None, None, 0, 0, series_wins4_rules,
                        r3_winners, 1, r3_winners, 2, champion, league, runner_up, league,
                        False, False)

playoff.series = [series1, series2, series3, series4, series5, series6, series7, series8, series9, series10, series11]

games = []
loop = 0

for league_rank in league.rankings:
    print(f'{league_rank.rank}. {league_rank.team.name}')

current_day = 1
days = {}
#  setup first round of playoff
while not playoff.is_complete():
    print(f'Current Round: {playoff.current_round}')
    while not playoff.is_round_complete(playoff.current_round):
        if not playoff.is_round_setup(playoff.current_round):
            playoff.setup_round(playoff.current_round)
        # print(loop)
        new_games = playoff.create_new_games(games)
        Scheduler.add_games_to_schedule(new_games, days, r, current_day)
        games.extend(new_games)
        for g in days[current_day]:
            g.play(r)
            model = GameService.game_to_vm(g)
            playoff.process_game(g)
            # print(GameView.get_basic_view(model))
        game_day_view_model = GameService.games_to_game_day_view(days[current_day])
        #print(GameDayView.get_view(game_day_view_model))
        current_day += 1

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
    playoff.post_process_round(playoff.current_round)
    playoff.current_round += 1

# post process the playoff
