import random

from teams.ConsoleUI.views.playoff_views import SeriesView
from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition import CompetitionTeam
from teams.domain.competition_configuration import CompetitionConfiguration, RankingGroupConfiguration, \
    SubCompetitionConfiguration, SeriesConfiguration, PlayoffSubCompetitionConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesRules, SeriesByWinsRules
from teams.domain.team import Team
from teams.services.game_service import GameService
from teams.services.view_models.playoff_view_models import SeriesViewModel
from teams.services.view_models.team_view_models import TeamViewModel

toronto = Team("Toronto", 5, True)
montreal = Team("Montreal", 5, True)
ottawa = Team("Ottawa", 5, True)
quebec_city = Team("Quebec City", 5, True)
calgary = Team("Calgary", 5, True)
edmonton = Team("Edmonton", 5, True)
vancouver = Team("Vancouver", 5, True)
winnipeg = Team("Winnipeg", 5, True)
victoria = Team("Victoria", 5, True)
saskatoon = Team("Saskatoon", 5, True)
hamilton = Team("Hamilton", 5, True)
halifax = Team("Halifax", 5, True)

teams = [toronto, montreal, ottawa, quebec_city, calgary, edmonton, vancouver, winnipeg, victoria, saskatoon, hamilton, halifax]

playoff_game_rules = GameRules("Playoff Rules", False)
series_rules = SeriesByWinsRules("Best of 7", 4, playoff_game_rules, [0, 0, 1, 1, 0, 1, 0])

competition_config = CompetitionConfiguration("Playoff Test", [], 1, 1, None)

playoff_config = PlayoffSubCompetitionConfiguration("Playoff", competition_config, [], [], 1, SubCompetitionConfiguration.PLAYOFF_TYPE, 1, None)
competition_config.sub_competitions.append(playoff_config)

# seeding group
league_config = RankingGroupConfiguration("League", playoff_config, None, 1, 1, None)

# playoff groups
r1_winners = RankingGroupConfiguration("R1 Winners", playoff_config, None, 1, 1, None)
r2_winners = RankingGroupConfiguration("R2 Winners", playoff_config, None, 1, 1, None)
champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)

group_configs = [league_config, r1_winners, r2_winners, champion, runner_up]

# round 1
r1s1 = SeriesConfiguration("R1S1", 1, playoff_config, league_config, 1, league_config, 8, series_rules, r1_winners, league_config, None, None, 1, None)
r1s2 = SeriesConfiguration("R1S2", 1, playoff_config, league_config, 2, league_config, 7, series_rules, r1_winners, league_config, None, None, 1, None)
r1s3 = SeriesConfiguration("R1S3", 1, playoff_config, league_config, 3, league_config, 6, series_rules, r1_winners, league_config, None, None, 1, None)
r1s4 = SeriesConfiguration("R1S4", 1, playoff_config, league_config, 4, league_config, 5, series_rules, r1_winners, league_config, None, None, 1, None)
# round 2
r2s1 = SeriesConfiguration("R2S1", 2, playoff_config, r1_winners, 1, r1_winners, 4, series_rules, r2_winners, league_config, None, None, 1, None)
r2s2 = SeriesConfiguration("R2S2", 2, playoff_config, r1_winners, 2, r1_winners, 3, series_rules, r2_winners, league_config, None, None, 1, None)
# round 3
r3s1 = SeriesConfiguration("R3S1", 3, playoff_config, r2_winners, 1, r2_winners, 2, series_rules, champion, league_config, runner_up, league_config, 1, None)

series_configs = [r1s1, r1s2, r1s3, r1s4, r2s2, r2s1, r3s1]
playoff_config.series = series_configs

current_groups = []

competition = CompetitionConfigurator.create_competition(competition_config, 1)
#playoff = CompetitionConfigurator.create_sub_competition(playoff_config, competition)
playoff = competition.sub_competitions[0]
league = CompetitionConfigurator.create_competition_group(league_config, current_groups, competition)

#for series_config in series_configs:
#    CompetitionConfigurator.process_series_configuration(series_config, current_groups, playoff)

r = random

comp_teams = [CompetitionTeam(competition, t) for t in teams]
r.shuffle(comp_teams)

count = 1
for team in comp_teams:
    league.add_team_to_group(team, count)
    count += 1

for league_rank in league.rankings:
    print(f'{league_rank.rank}. {league_rank.team.name}')

current_day = 1
days = {}
games = []
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

