import random

from teams.ConsoleUI.views.game_view import GameDayView
from teams.ConsoleUI.views.record_view import RecordView
from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_configuration import CompetitionConfiguration, TableSubCompetitionConfiguration, \
    RankingGroupConfiguration, CompetitionTeamConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.sub_competition import TableSubCompetition
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from tests.teams.domain.competition.testing_sample_data import western_teams, eastern_teams, pacific_teams, teams, \
    central_teams, atlantic_teams, north_teams

season_game_rules = GameRules("Season Rules", True)

competition_config = CompetitionConfiguration("Table Test", [], [], 1, 1, None)

table_config = TableSubCompetitionConfiguration("Table League", competition_config, [], [], 1, 1, None)
competition_config.sub_competition_configurations.append(table_config)

team_configs = []
# seeding group
league_config = RankingGroupConfiguration("League", table_config, None, 1, 1, None)
western_config = RankingGroupConfiguration("Western", table_config, None, 1, 1, None)
eastern_config = RankingGroupConfiguration("Eastern", table_config, None, 1, 1, None)
pacific_config = RankingGroupConfiguration("Pacific", table_config, None, 1, 1, None)
central_config = RankingGroupConfiguration("Central", table_config, None, 1, 1, None)
atlantic_config = RankingGroupConfiguration("Atlantic", table_config, None, 1, 1, None)
north_config = RankingGroupConfiguration("North", table_config, None, 1, 1, None)

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

table_config.competition_groups = [league_config, western_config, eastern_config, pacific_config, central_config, north_config, atlantic_config]

competition = CompetitionConfigurator.setup_competition(competition_config, 1)
table = competition.sub_competition_configurations[0]

r = random

rankings = []
for g in table.groups:
    rankings.extend(g.rankings)

scheduler = Scheduler()
games = scheduler.schedule_games(competition.team_configurations, season_game_rules, 1, 1, True, table.create_game)
days = Scheduler.organize_games_into_days(games)

for cg in [competition.get_group_by_name(western_config.name),
           competition.get_group_by_name(eastern_config.name)]:
    cg_teams = [r.team for r in cg.rankings]
    for i in range(2):
        new_games = scheduler.schedule_games(cg_teams, season_game_rules, 1, 1, True, table.create_game)
        new_days = Scheduler.organize_games_into_days(new_games)
        for day in new_days.keys():
            Scheduler.add_day_to_scheduler(new_days[day], days, 1)

#for cg in [competition.get_group_by_name(pacific_config.name),
#           competition.get_group_by_name(central_config.name),
#           competition.get_group_by_name(atlantic_config.name),
#           competition.get_group_by_name(north_config.name)]:
#    cg_teams = [r.team for r in cg.rankings]
#    new_games = scheduler.schedule_games(cg_teams, season_game_rules, 1, 1, True, table.create_game)
#    new_days = Scheduler.organize_games_into_days(new_games)
#    for day in new_days.keys():
#        Scheduler.add_day_to_scheduler(new_days[day], days, 1)


for d in days.keys():
    day = days[d]
    for g in day:
        g.play(r)
        competition.process_game(g)
    game_day_view_model = GameService.games_to_game_day_view(day)
    print(GameDayView.get_view(game_day_view_model))

table.sort_rankings(rankings, table.records)
league = competition.get_group_by_name(league_config.name)

recs = TableSubCompetition.get_records_by_group(league, table.records)
recs.sort(key=lambda rec: rec.rank)

print(RecordView.get_table_header())
for r in recs:
    print(RecordView.get_table_row(RecordService.get_view_from_model(r)))