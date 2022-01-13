import random

from teams.ConsoleUI.views.playoff_views import SeriesView
from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_configuration import CompetitionConfiguration, RankingGroupConfiguration, \
    SeriesConfiguration, PlayoffSubCompetitionConfiguration, CompetitionTeamConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByWinsRules
from teams.services.game_service import GameService
from teams.services.view_models.playoff_view_models import SeriesViewModel
from teams.services.view_models.team_view_models import TeamViewModel
from tests.teams.domain.competition.testing_sample_data import western_teams, eastern_teams, pacific_teams, teams, \
    central_teams, atlantic_teams, north_teams

playoff_game_rules = GameRules("Playoff Rules", False)
series_rules = SeriesByWinsRules("Best of 7", 4, playoff_game_rules, [0, 0, 1, 1, 0, 1, 0])
series_rules_3 = SeriesByWinsRules("Best of 3", 2, playoff_game_rules, [0, 0, 1])

competition_config = CompetitionConfiguration("Playoff Test", [], [], 1, 1, None)

playoff_config = PlayoffSubCompetitionConfiguration("Playoff", competition_config, [], [], [], 1, 1, None)
competition_config.sub_competition_configurations.append(playoff_config)

team_configs = []
# seeding group
league_config = RankingGroupConfiguration("League", playoff_config, None, 1, 1, None)
western_config = RankingGroupConfiguration("Western", playoff_config, None, 1, 1, None)
eastern_config = RankingGroupConfiguration("Eastern", playoff_config, None, 1, 1, None)
pacific_config = RankingGroupConfiguration("Pacific", playoff_config, None, 1, 1, None)
central_config = RankingGroupConfiguration("Central", playoff_config, None, 1, 1, None)
atlantic_config = RankingGroupConfiguration("Atlantic", playoff_config, None, 1, 1, None)
north_config = RankingGroupConfiguration("North", playoff_config, None, 1, 1, None)
for t in teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, league_config, 1, None))
for t in western_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, western_config, 1, None))
for t in eastern_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, eastern_config, 1, None))
for t in pacific_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, pacific_config, 1, None))
for t in central_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, central_config, 1, None))
for t in atlantic_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, atlantic_config, 1, None))
for t in north_teams:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, north_config, 1, None))

competition_config.team_configurations = team_configs

# playoff groups
west_q1_winners = RankingGroupConfiguration("West Q1 Winners", playoff_config, None, 1, 1, None)
east_q1_winners = RankingGroupConfiguration("East Q1 Winners", playoff_config, None, 1, 1, None)
r1_winners = RankingGroupConfiguration("R1 Winners", playoff_config, None, 1, 1, None)
west_r1_winners = RankingGroupConfiguration("West R1 Winners", playoff_config, None, 1, 1, None)
pacific_q1_winners = RankingGroupConfiguration("Pacific Q1 Winners", playoff_config, None, 1, 1, None)
central_q1_winners = RankingGroupConfiguration("Central Q1 Winners", playoff_config, None, 1, 1, None)
east_r1_winners = RankingGroupConfiguration("East R1 Winners", playoff_config, None, 1, 1, None)
r2_winners = RankingGroupConfiguration("R2 Winners", playoff_config, None, 1, 1, None)
west_r2_winners = RankingGroupConfiguration("West R2 Winners", playoff_config, None, 1, 1, None)
pacific_r1_winners = RankingGroupConfiguration("Pacific R1 Winners", playoff_config, None, 1, 1, None)
central_r1_winners = RankingGroupConfiguration("Central R1 Winners", playoff_config, None, 1, 1, None)
pacific_r2_winners = RankingGroupConfiguration("Pacific R2 Winners", playoff_config, None, 1, 1, None)
central_r2_winners = RankingGroupConfiguration("Central R2 Winners", playoff_config, None, 1, 1, None)
east_r2_winners = RankingGroupConfiguration("East R2 Winners", playoff_config, None, 1, 1, None)
r3_winners = RankingGroupConfiguration("R3 Winners", playoff_config, None, 1, 1, None)
champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)

playoff_config.competition_groups = [league_config, western_config, eastern_config, pacific_config, central_config, north_config, atlantic_config,
                                     west_q1_winners, east_q1_winners, pacific_q1_winners, central_q1_winners,
                                     r1_winners, west_r1_winners, east_r1_winners, pacific_r1_winners, central_r1_winners,
                                     west_r2_winners, east_r2_winners, r2_winners,
                                     r3_winners,
                                     champion, runner_up]
# qualifying
rqs1 = SeriesConfiguration("RQS1", 1, playoff_config, pacific_config, 4, pacific_config, 5, series_rules_3, pacific_q1_winners, league_config, None, None, 1, None)
rqs2 = SeriesConfiguration("RQS2", 1, playoff_config, central_config, 4, central_config, 5, series_rules_3, central_q1_winners, league_config, None, None, 1, None)
rqs3 = SeriesConfiguration("RQS3", 1, playoff_config, atlantic_config, 4, atlantic_config, 5, series_rules_3, east_q1_winners, league_config, None, None, 1, None)
rqs4 = SeriesConfiguration("RQS4", 1, playoff_config, north_config, 4, north_config, 5, series_rules_3, east_q1_winners, league_config, None, None, 1, None)
# round 1
r1s1 = SeriesConfiguration("R1S1", 2, playoff_config, pacific_config, 1, pacific_q1_winners, 1, series_rules, pacific_r1_winners, league_config, None, None, 1, None)
r1s2 = SeriesConfiguration("R1S2", 2, playoff_config, pacific_config, 2, pacific_config, 3, series_rules, pacific_r1_winners, league_config, None, None, 1, None)
r1s3 = SeriesConfiguration("R1S3", 2, playoff_config, central_config, 1, central_q1_winners, 1, series_rules, central_r1_winners, league_config, None, None, 1, None)
r1s4 = SeriesConfiguration("R1S4", 2, playoff_config, central_config, 2, central_config, 3, series_rules, central_r1_winners, league_config, None, None, 1, None)
r1s5 = SeriesConfiguration("R1S5", 2, playoff_config, eastern_config, 1, east_q1_winners, 2, series_rules, east_r1_winners, league_config, None, None, 1, None)
r1s6 = SeriesConfiguration("R1S6", 2, playoff_config, eastern_config, 2, east_q1_winners, 1, series_rules, east_r1_winners, league_config, None, None, 1, None)
r1s7 = SeriesConfiguration("R1S7", 2, playoff_config, eastern_config, 3, eastern_config, 6, series_rules, east_r1_winners, league_config, None, None, 1, None)
r1s8 = SeriesConfiguration("R1S8", 2, playoff_config, eastern_config, 4, eastern_config, 5, series_rules, east_r1_winners, league_config, None, None, 1, None)
# round 2
r2s1 = SeriesConfiguration("R2S1", 3, playoff_config, pacific_r1_winners, 1, pacific_r1_winners, 2, series_rules, west_r2_winners, league_config, None, None, 1, None)
r2s2 = SeriesConfiguration("R2S2", 3, playoff_config, central_r1_winners, 1, central_r1_winners, 2, series_rules, west_r2_winners, league_config, None, None, 1, None)
r2s3 = SeriesConfiguration("R2S3", 3, playoff_config, east_r1_winners, 1, east_r1_winners, 3, series_rules, east_r2_winners, league_config, None, None, 1, None)
r2s4 = SeriesConfiguration("R2S4", 3, playoff_config, east_r1_winners, 2, east_r1_winners, 4, series_rules, east_r2_winners, league_config, None, None, 1, None)
# round 3
r3s1 = SeriesConfiguration("R3S1", 4, playoff_config, west_r2_winners, 1, west_r2_winners, 2, series_rules, r3_winners, league_config, None, None, 1, None)
r3s2 = SeriesConfiguration("R3S2", 4, playoff_config, east_r2_winners, 1, east_r2_winners, 2, series_rules, r3_winners, league_config, None, None, 1, None)
# Final
r4s1 = SeriesConfiguration("R4S1", 5, playoff_config, r3_winners, 1, r3_winners, 2, series_rules, champion, league_config, runner_up, league_config, 1, None)

playoff_config.series_configurations = [r1s1, r1s2, r1s3, r1s4, r1s5, r1s6, r1s7, r1s8, r2s1, r2s2, r2s3, r2s4, r3s1, r3s2, r4s1, rqs1, rqs2, rqs3, rqs4]

competition = CompetitionConfigurator.setup_competition(competition_config, 1)
playoff = competition.sub_competition_configurations[0]
league = competition.get_group_by_name(league_config.name)
western = competition.get_group_by_name(western_config.name)
eastern = competition.get_group_by_name(eastern_config.name)
pacific = competition.get_group_by_name(pacific_config.name)
central = competition.get_group_by_name(central_config.name)
atlantic = competition.get_group_by_name(atlantic_config.name)
north = competition.get_group_by_name(north_config.name)

r = random

r.shuffle(competition.team_configurations)
ranks = {}
count = 1
for t in teams:
    ranks[t.name] = count
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
            competition.process_game(g)
            # print(GameView.get_basic_view(model))
        game_day_view_model = GameService.games_to_game_day_view(days[current_day])
        #print(GameDayView.get_view(game_day_view_model))
        current_day += 1

    for s in [ps for ps in playoff.series_configurations if ps.series_round == playoff.current_round]:
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

champion = competition.get_group_by_name("Champion")
runner_up = competition.get_group_by_name("Runner Up")
print("")
print(f"Champion: {champion.rankings[0].team.name:15} Runner Up: {runner_up.rankings[0].team.name:15}")

