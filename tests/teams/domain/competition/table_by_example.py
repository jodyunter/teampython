import random

from teams.ConsoleUI.views.record_view import RecordView
from teams.domain.competition import Competition, CompetitionGroup, TableRecord
from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.sub_competition import TableSubCompetition
from teams.services.record_service import RecordService
from tests.teams.domain.competition import helpers

competition = Competition("My Comp", 5, [], False, False, False, False)

table = TableSubCompetition("Table", [], competition, 1, True, True, False, False)

teams = [
    helpers.new_comp_team(competition, "Team 1", 5),
    helpers.new_comp_team(competition, "Team 2", 5),
    helpers.new_comp_team(competition, "Team 3", 5),
    helpers.new_comp_team(competition, "Team 4", 5),
    helpers.new_comp_team(competition, "Team 5", 5),
    helpers.new_comp_team(competition, "Team 6", 5),
    helpers.new_comp_team(competition, "Team 7", 5),
    helpers.new_comp_team(competition, "Team 8", 5),
    helpers.new_comp_team(competition, "Team 9", 5),
    helpers.new_comp_team(competition, "Team 10", 5),
    helpers.new_comp_team(competition, "Team 11", 5),
    helpers.new_comp_team(competition, "Team 12", 5),
]

league = CompetitionGroup("League", None, table, [], CompetitionGroupConfiguration.RANKING_TYPE)
[league.add_team_to_group(t) for t in teams]
west = CompetitionGroup("West", league, table, [], CompetitionGroupConfiguration.RANKING_TYPE)
east = CompetitionGroup("East", league, table, [], CompetitionGroupConfiguration.RANKING_TYPE)

table.records = [TableRecord(table, -1, t, table.competition.year, 0, 0, 0, 0, 0, 5) for t in teams]

for i in range(len(teams)):
    group = None
    if i % 2 == 0:
        group = west
    else:
        group = east

    group.add_team_to_group(teams[i])

rankings = []
rankings.extend(league.rankings)
rankings.extend(west.rankings)
rankings.extend(east.rankings)

game_rules = GameRules("Season", True)

scheduler = Scheduler()
games = scheduler.schedule_games(teams, game_rules, 5, 1, True, table.create_game)

r = random
for g in games:
    g.play(r)
    table.process_game(g)

table.sort_rankings(rankings, table.records)

for r in table.records:
    print(RecordView.get_table_row(RecordService.get_view_from_model(r)))


