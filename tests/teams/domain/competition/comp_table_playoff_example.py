import random

from teams.ConsoleUI.views.game_view import GameDayView
from teams.ConsoleUI.views.playoff_views import SeriesView
from teams.ConsoleUI.views.record_view import RecordView
from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_configuration import RankingGroupConfiguration, CompetitionConfiguration, \
    TableSubCompetitionConfiguration, CompetitionTeamConfiguration, PlayoffSubCompetitionConfiguration, \
    SeriesConfiguration
from teams.domain.game import GameRules
from teams.domain.scheduler import Scheduler
from teams.domain.series import SeriesByWins, SeriesByGoals
from teams.domain.series_rules import SeriesByWinsRules
from teams.domain.sub_competition import TableSubCompetition
from teams.domain.team import Team
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from teams.services.view_models.playoff_view_models import SeriesViewModel
from teams.services.view_models.team_view_models import TeamViewModel

toronto = Team("Toronto", 5, True)
montreal = Team("Montreal", 5, True)
ottawa = Team("Ottawa", 5, True)
vancouver = Team("Vancouver", 5, True)
calgary = Team("Calgary", 5, True)
edmonton = Team("Edmonton", 5, True)

season_game_rules = GameRules("Season Rules", True)
playoff_game_rules = GameRules("Playoff Rules", False)
series_rules = SeriesByWinsRules("Best of 3", 2, playoff_game_rules, [0, 1, 0])

competition_config = CompetitionConfiguration("Test", [], [], 1, 1, None)

# table config
table_config = TableSubCompetitionConfiguration("My League", competition_config, [], [], 1, 1, None)
competition_config.sub_competitions.append(table_config)

league_config = RankingGroupConfiguration("League", table_config, None, 1, 1, None)
western_config = RankingGroupConfiguration("Western", table_config, None, 1, 1, None)
eastern_config = RankingGroupConfiguration("Eastern", table_config, None, 1, 1, None)

team_configs = []
for t in [calgary, edmonton, toronto, montreal, ottawa, vancouver]:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, league_config, 1, None))
for t in [calgary, edmonton, vancouver]:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, western_config, 1, None))
for t in [toronto, montreal, ottawa]:
    team_configs.append(CompetitionTeamConfiguration(t, competition_config, eastern_config, 1, None))

competition_config.teams = team_configs

table_config.competition_groups = [league_config, western_config, eastern_config]

# playoff config
playoff_config = PlayoffSubCompetitionConfiguration("Playoff", competition_config, [], [], [], 1, 1, None)
competition_config.sub_competitions.append(playoff_config)

r1_winners = RankingGroupConfiguration("R1 Winners", playoff_config, None, 1, 1, None)
champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)

playoff_config.competition_groups = [r1_winners, champion, runner_up]

# round 1
r1s1 = SeriesConfiguration("R1S1", 1, playoff_config, western_config, 1, eastern_config, 2, series_rules, r1_winners, league_config, None, None, 1, None)
r1s2 = SeriesConfiguration("R1S2", 1, playoff_config, eastern_config, 1, western_config, 2, series_rules, r1_winners, league_config, None, None, 1, None)

# Final
final = SeriesConfiguration("Final", 2, playoff_config, r1_winners, 1, r1_winners, 2, series_rules, champion, league_config, runner_up, league_config, 1, None)

series_config = [r1s1, r1s2, final]
playoff_config.series = series_config
# configuration done

competition = CompetitionConfigurator.create_competition(competition_config, 1)
table = competition.get_sub_competition(table_config.name)
playoff = competition.get_sub_competition(playoff_config.name)

rand = random

rankings = []
for g in table.groups:
    rankings.extend(g.rankings)

#  schedule the games, need to move this to the configuration when the season is setup
scheduler = Scheduler()
games = scheduler.schedule_games(competition.teams, season_game_rules, 1, 1, True, table.create_game)
days = Scheduler.organize_games_into_days(games)

for cg in [competition.get_group_by_name(western_config.name),
           competition.get_group_by_name(eastern_config.name)]:
    cg_teams = [r.team for r in cg.rankings]
    for i in range(5):
        new_games = scheduler.schedule_games(cg_teams, season_game_rules, 1, 1, True, table.create_game)
        new_days = Scheduler.organize_games_into_days(new_games)
        for day in new_days.keys():
            Scheduler.add_day_to_scheduler(new_days[day], days, 1)


for d in days.keys():
    day = days[d]
    for g in day:
        g.play(rand)
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

current_day = d + 1
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
        Scheduler.add_games_to_schedule(new_games, days, rand, current_day)
        games.extend(new_games)
        for g in days[current_day]:
            g.play(rand)
            model = GameService.game_to_vm(g)
            competition.process_game(g)
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

champion = competition.get_group_by_name("Champion")
runner_up = competition.get_group_by_name("Runner Up")
print("")
print(f"Champion: {champion.rankings[0].team.name:15} Runner Up: {runner_up.rankings[0].team.name:15}")
