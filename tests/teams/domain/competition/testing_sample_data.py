import random

from teams.ConsoleUI.views.game_view import GameDayView
from teams.ConsoleUI.views.record_view import RecordView
from teams.data.database import Database
from teams.data.repo.competition_configuration_repository import CompetitionConfigurationRepository, \
    TableSubCompetitionConfigurationRepository, RankingGroupConfigurationRepository, \
    CompetitionTeamConfigurationRepository
from teams.data.repo.competition_repository import CompetitionRepository
from teams.data.repo.rules_repository import GameRulesRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain import CompetitionConfiguration, TableSubCompetitionConfiguration, CompetitionTeamConfiguration, \
    GameRules, TableSubCompetition
from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_group_configuration import RankingGroupConfiguration
from teams.domain.scheduler import Scheduler
from teams.domain.team import Team
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService


def create_games(groups, rounds, rules, create_game_method, day_dict, scheduler):
    games = []
    for cg in groups:
        cg_teams = [r.team for r in cg.rankings]
        for i in range(rounds):
            next_games = scheduler.schedule_games(cg_teams, rules, 1, 1, True, create_game_method)
            games.extend(next_games)
            new_days = Scheduler.organize_games_into_days(next_games)
            for new_day in new_days.keys():
                Scheduler.add_day_to_scheduler(new_days[new_day], day_dict, 1)
    return games


def print_group(group_name, table_to_print, description):
    group = competition.get_group_by_name(group_name)

    recs = TableSubCompetition.get_records_by_group(group, table_to_print.records)
    recs.sort(key=lambda rec: rec.rank)

    print(description)
    print(RecordView.get_table_header())
    for r in recs:
        print(RecordView.get_table_row(RecordService.get_view_from_model(r)))

connection = "sqlite:///:memory:"
Database.init_db(connection)
session = Database.get_session()
Database.clean_up_database(session)
session.commit()

team_data = {
    "Toronto": [5, True],
    "Montreal": [5, True],
    "Ottawa": [5, True],
    "Winnipeg": [5, True],
    "Calgary": [5, True],
    "Vancouver": [5, True]
}
skill = 0
active = 1

teams = ["Toronto", "Montreal", "Ottawa", "Winnipeg", "Calgary", "Vancouver"]

team_service = TeamService()
team_repo = TeamRepository()
game_rules_repo = GameRulesRepository()

competition_config_repo = CompetitionConfigurationRepository()
table_config_repo = TableSubCompetitionConfigurationRepository()
ranking_group_config_repo = RankingGroupConfigurationRepository()
competition_team_config_repo = CompetitionTeamConfigurationRepository()

game_rules_repo.add(GameRules("Season Rules", True), session)
session.commit()

# create all the teams
for t in team_data:
    team_service.create(t, team_data[t][skill], team_data[t][active])

# create the competition configuration
competition_config = CompetitionConfiguration("League Configuration", [], [], 1, 1, None)
competition_config_repo.add(competition_config, session)
session.commit()

# create the sub competition configurations
table_configuration = TableSubCompetitionConfiguration("Standings", competition_config, [], 1, 1, None)
table_config_repo.add(table_configuration, session)
session.commit()

# ranking groups/division configuration
premier_division_config = RankingGroupConfiguration("Premier", table_configuration, None, 1, 1, None)
ranking_group_config_repo.add(premier_division_config, session)
session.commit()

# create the team configurations
# premier has all
[competition_team_config_repo.add(
    CompetitionTeamConfiguration(team, competition_config, premier_division_config, 1, None), session)
    for team in [team_repo.get_by_name(name, session) for name in teams]]
session.commit()


comp_config = competition_config_repo.get_by_oid(competition_config.oid, session)

competition = CompetitionConfigurator.setup_competition(comp_config, 1)

# get initial games.  For tables we can't really do this yet.
days = {}  # this is inplace of the database for now
scheduler = Scheduler()

standings_table = competition.get_sub_competition("Standings")

games = []
season_rules = game_rules_repo.get_by_name("Season Rules", session)

games.extend(
    create_games(standings_table.get_groups_by_level(1), 2, season_rules, standings_table.create_game, days,
                 scheduler))


competition.start_competition()

comp_repo = CompetitionRepository()
comp_repo.add(competition, session)
session.commit()

last_day = 1
current_day = 1

rand = random

while not competition.finished:
    print("Current Comp Round: " + str(competition.current_round))
    new_games = competition.create_new_games(current_games=games)
    Scheduler.add_games_to_schedule(new_games, days, rand, current_day)
    games.extend(new_games)
    if current_day in days:
        day = days[current_day]
        for g in day:
            g.play()
            competition.process_game(g)
        competition.process_end_of_day(competition.sort_day_dictionary_to_incomplete_games_dictionary(days))
        game_day_view_model = GameService.games_to_game_day_view(day)
        print(GameDayView.get_view(game_day_view_model))
    else:
        day = []
    last_day = current_day
    current_day += 1

standings_table.sort_table_rankings()

print_group("Premier", standings_table, "Standings")

session.commit()

recordService = RecordService()
for r in recordService.get_all(session):
    print(r.name + " " + r.points)