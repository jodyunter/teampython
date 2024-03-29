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


def create_games(groups, rounds, rules, create_game_method, day_dict):
    for cg in groups:
        cg_teams = [r.team for r in cg.rankings]
        for i in range(rounds):
            next_games = scheduler.schedule_games(cg_teams, rules, 1, 1, True, create_game_method)
            new_days = Scheduler.organize_games_into_days(next_games)
            for new_day in new_days.keys():
                Scheduler.add_day_to_scheduler(new_days[new_day], day_dict, 1)


def print_group(group_name, table_to_print, description):
    group = competition.get_group_by_name(group_name)

    recs = TableSubCompetition.get_records_by_group(group, table_to_print.records)
    recs.sort(key=lambda rec: rec.rank)

    print(description)
    print(RecordView.get_table_header())
    for r in recs:
        print(RecordView.get_table_row(RecordService.get_view_from_model(r)))


def setup_config(rand, canadian_league_name, american_league_name, playoff_name, season_game_rules, playoff_game_rules):
    min_skill = 0
    max_skill = 10
    toronto = Team("Toronto", rand.randint(min_skill, max_skill), True)
    montreal = Team("Montreal", rand.randint(min_skill, max_skill), True)
    ottawa = Team("Ottawa", rand.randint(min_skill, max_skill), True)
    quebec_city = Team("Quebec City", rand.randint(min_skill, max_skill), True)

    vancouver = Team("Vancouver", rand.randint(min_skill, max_skill), True)
    calgary = Team("Calgary", rand.randint(min_skill, max_skill), True)
    edmonton = Team("Edmonton", rand.randint(min_skill, max_skill), True)
    winnipeg = Team("Winnipeg", rand.randint(min_skill, max_skill), True)

    boston = Team("Boston", rand.randint(min_skill, max_skill), True)
    detroit = Team("Detroit", rand.randint(min_skill, max_skill), True)
    new_york = Team("New York", rand.randint(min_skill, max_skill), True)

    series_rules = SeriesByWinsRules("Best of 7", 4, playoff_game_rules, [0, 0, 1, 1, 0, 1, 0])
    series_rules_2 = SeriesByWinsRules("Best of 3", 2, playoff_game_rules, [1, 0, 0])

    competition_config = CompetitionConfiguration("Test", [], [], 1, 1, None)

    # table config
    canadian_table_config = TableSubCompetitionConfiguration(canadian_league_name, competition_config, [], [], 1, 1, None)
    american_table_config = TableSubCompetitionConfiguration(american_league_name, competition_config, [], [], 1, 1,
                                                             None)
    competition_config.sub_competitions.append(canadian_table_config)
    competition_config.sub_competitions.append(american_table_config)

    canadian_config = RankingGroupConfiguration("Canadian", canadian_table_config, None, 1, 1, None)
    western_config = RankingGroupConfiguration("Western", canadian_table_config, canadian_config, 2, 1, None)
    eastern_config = RankingGroupConfiguration("Eastern", canadian_table_config, canadian_config, 2, 1, None)

    american_config = RankingGroupConfiguration("American", american_table_config, None, 1, 1, None)

    all_teams = [calgary, edmonton, toronto, montreal, ottawa, vancouver, quebec_city, winnipeg, boston, detroit, new_york]
    western_teams = [calgary, edmonton, vancouver, winnipeg]
    eastern_teams = [toronto, montreal, ottawa, quebec_city]
    american_teams = [boston, detroit, new_york]
    canadian_teams = [calgary, edmonton, toronto, montreal, ottawa, vancouver, quebec_city, winnipeg]

    team_group_map = {
        western_config.name: {"config": western_config, "teams": western_teams, "sub_comp": canadian_table_config},
        eastern_config.name: {"config": eastern_config, "teams": eastern_teams, "sub_comp": canadian_table_config},
        american_config.name: {"config": american_config, "teams": american_teams, "sub_comp": american_table_config},
        canadian_config.name: {"config": canadian_config, "teams": canadian_teams, "sub_comp": canadian_table_config}
    }

    team_configs = []

    for key in team_group_map.keys():
        config = team_group_map[key]["config"]
        teams = team_group_map[key]["teams"]
        sub_comp = team_group_map[key]["sub_comp"]
        for t in teams:
            team_configs.append(CompetitionTeamConfiguration(t, competition_config, config, 1, None))

        sub_comp.competition_groups.append(config)

    competition_config.teams = team_configs

    # playoff config
    playoff_config = PlayoffSubCompetitionConfiguration(playoff_name, competition_config, [], [], [], 1, 1, None)
    competition_config.sub_competitions.append(playoff_config)

    r1_winners = RankingGroupConfiguration("R1 Winners", playoff_config, None, 1, 1, None)
    american_rep = RankingGroupConfiguration("American Champion", playoff_config, None, 1, 1, None)
    champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
    runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)
    can_am_winners = RankingGroupConfiguration("CanAm Challenge Winners", playoff_config, None, 1, 1, None)

    playoff_config.competition_groups = [r1_winners, champion, runner_up, american_rep]

    # round 1
    r1s1 = SeriesConfiguration("R1S1", 1, playoff_config, western_config, 1, eastern_config, 2, series_rules, r1_winners,
                               canadian_config, None, None, 1, None)
    r1s2 = SeriesConfiguration("R1S2", 1, playoff_config, eastern_config, 1, western_config, 2, series_rules, r1_winners,
                               canadian_config, None, None, 1, None)

    r1s3 = SeriesConfiguration("AMF", 1, playoff_config, american_config, 1, american_config, 2, series_rules, american_rep,
                               american_config, None, None, 1, None)
    # Final
    final = SeriesConfiguration("Final", 2, playoff_config, r1_winners, 1, r1_winners, 2, series_rules, champion,
                                canadian_config, runner_up, canadian_config, 1, None)

    # misc
    can_am = SeriesConfiguration("CanAm", 3, playoff_config, canadian_config, 8, american_rep, 1,
                                 series_rules_2, can_am_winners, None, None, None, 1, None)

    series_config = [r1s1, r1s2, r1s3, final, can_am]

    playoff_config.series = series_config
    # configuration done

    return competition_config


season_game_rules = GameRules("Season Rules", True)
playoff_game_rules = GameRules("Playoff Rules", False)

rand = random
canadian_league_name = "Canadian League"
american_league_name = "American League"
playoff_name = "Playoff"

competition_config = setup_config(rand, canadian_league_name, american_league_name, playoff_name, season_game_rules, playoff_game_rules)

competition = CompetitionConfigurator.setup_competition(competition_config, 1)
canadian_table = competition.get_sub_competition(canadian_league_name)
american_table = competition.get_sub_competition(american_league_name)

playoff = competition.get_sub_competition(playoff_name)

#  schedule the games, need to move this to the configuration when the season is setup
scheduler = Scheduler()
days = {}

level_1_rounds = 1
level_2_rounds = 5


create_games(canadian_table.get_groups_by_level(1), 2, season_game_rules, canadian_table.create_game, days)
create_games(american_table.get_groups_by_level(1), 6, season_game_rules, american_table.create_game, days)
create_games(canadian_table.get_groups_by_level(2), 4, season_game_rules, canadian_table.create_game, days)

last_day = -1

for d in days.keys():
    day = days[d]
    for g in day:
        g.play()
        competition.process_game(g)
    competition.process_end_of_day(competition.sort_day_dictionary_to_incomplete_games_dictionary(days))
    game_day_view_model = GameService.games_to_game_day_view(day)
    print(GameDayView.get_view(game_day_view_model))
    last_day = d

canadian_table.sort_table_rankings()
american_table.sort_table_rankings()

print_group("Canadian", canadian_table, "League")
for g in competition.get_groups_by_level_and_comp(2, canadian_league_name):
    print_group(g.name, canadian_table, g.name)

print_group("American", american_table, "American")

current_day = last_day + 1
days = {}
games = []
#  setup first round of playoff
while not playoff.is_complete():
    print(f'Current Round: {playoff.current_round}')
    while not playoff.is_round_complete(playoff.current_round):
        if not playoff.is_round_setup(playoff.current_round):
            playoff.setup_round(playoff.current_round)
        # print(loop)
        new_games = playoff.create_new_games(current_games=games)
        Scheduler.add_games_to_schedule(new_games, days, rand, current_day)
        games.extend(new_games)
        for g in days[current_day]:
            g.play()
            model = GameService.game_to_vm(g)
            competition.process_game(g)
            # print(GameView.get_basic_view(model))
        game_day_view_model = GameService.games_to_game_day_view(days[current_day])
        # print(GameDayView.get_view(game_day_view_model))
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


