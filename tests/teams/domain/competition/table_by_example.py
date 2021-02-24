import random

from teams.ConsoleUI.views.game_view import GameDayView
from teams.ConsoleUI.views.record_view import RecordView
from teams.domain.competition import Competition, TableRecord, RankingGroup
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.sub_competition import TableSubCompetition
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from tests.teams.domain.competition import helpers


def add_teams_to_group(group, teams_to_add):
    for t in teams_to_add:
        group.add_team_to_group(t)


competition = Competition("My Comp", 5, [], [], False, False, False, False)

table = TableSubCompetition("Table", [], competition, 1, True, True, False, False)

toronto = helpers.new_comp_team(competition, "Toronto", 5)
montreal = helpers.new_comp_team(competition, "Montreal", 5)
quebec_city = helpers.new_comp_team(competition, "Quebec City", 5)
ottawa = helpers.new_comp_team(competition, "Ottawa", 5)
hamilton = helpers.new_comp_team(competition, "Hamilton", 5)
winnipeg = helpers.new_comp_team(competition, "Winnipeg", 5)
calgary = helpers.new_comp_team(competition, "Calgary", 5)
edmonton = helpers.new_comp_team(competition, "Edmonton", 5)
vancouver = helpers.new_comp_team(competition, "Vancouver", 5)

teams = [toronto, montreal, quebec_city, ottawa, winnipeg, calgary, edmonton, vancouver, hamilton]
west_teams = [winnipeg, calgary, edmonton, vancouver]
east_teams = [toronto, montreal, quebec_city, ottawa, hamilton]
pacific_teams = [vancouver, edmonton]
central_teams = [calgary, winnipeg]
ontario_teams = [ottawa, toronto, hamilton]
quebec_teams = [quebec_city, montreal]

league = RankingGroup("League", None, table, [])
[league.add_team_to_group(t) for t in teams]
west = RankingGroup("West", league, table, [])
east = RankingGroup("East", league, table, [])
pacific = RankingGroup("Pacific", west, table, [])
central = RankingGroup("Central", west, table, [])
ontario = RankingGroup("Atlantic", east, table, [])
quebec = RankingGroup("Quebec", east, table, [])

add_teams_to_group(league, teams)
add_teams_to_group(west, west_teams)
add_teams_to_group(east, east_teams)
add_teams_to_group(pacific, pacific_teams)
add_teams_to_group(central, central_teams)
add_teams_to_group(ontario, ontario_teams)
add_teams_to_group(quebec, quebec_teams)

groups = [league, west, east, pacific, central, ontario, quebec]

table.records = [TableRecord(table, -1, t, table.competition.year, 0, 0, 0, 0, 0, 5) for t in teams]

rankings = []
for g in groups:
    rankings.extend(g.rankings)

game_rules = GameRules("Season", True)
r = random

scheduler = Scheduler()
games = scheduler.schedule_games(teams, game_rules, 1, 1, True, table.create_game)
days = Scheduler.organize_games_into_days(games)

new_games = scheduler.schedule_games(teams, game_rules, 1, 1, True, table.create_game)
new_days = Scheduler.organize_games_into_days(new_games)
for day in new_days.keys():
    Scheduler.add_day_to_scheduler(new_days[day], days, 1)

#Scheduler.add_games_to_schedule(new_games, days, r, 1)

for d in days.keys():
    day = days[d]
    for g in day:
        g.play(r)
        table.process_game(g)
    game_day_view_model = GameService.games_to_game_day_view(day)
    print(GameDayView.get_view(game_day_view_model))

table.sort_rankings(rankings, table.records)

recs = TableSubCompetition.get_records_by_group(league, table.records)
recs.sort(key=lambda rec: rec.rank)

print(RecordView.get_table_header())
for r in recs:
    print(RecordView.get_table_row(RecordService.get_view_from_model(r)))




