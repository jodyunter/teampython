import numpy as np

from app_config import db_connection_string
from teams.data.database import Database
from teams.domain.competition_configuration import CompetitionConfiguration, TableSubCompetitionConfiguration, \
    RankingGroupConfiguration, CompetitionTeamConfiguration, PlayoffSubCompetitionConfiguration, SeriesConfiguration
from teams.services.app_service import AppService
from teams.services.configuration_service import ConfigurationService
from teams.services.game_service import GameRulesService
from teams.services.team_service import TeamService

setup = True

Database.init_db(db_connection_string)

# services
app_service = AppService()
game_rules_service = GameRulesService()
team_service = TeamService()
config_service = ConfigurationService()


def setup():
    game_rules_service.create("Season", True)
    game_rules_service.create("Playoff", False)
    app_service.setup_data(0, 0, True, True)
    setup_teams()


all_teams = ["Toronto", "Montreal", "Ottawa", "Quebec City", "Vancouver", "Calgary", "Edmonton", "Winnipeg"]
western_teams = ["Vancouver", "Calgary", "Edmonton", "Winnipeg"]
eastern_teams = ["Toronto", "Montreal", "Ottawa", "Quebec City"]


def setup_teams():
    min_skill = 0
    max_skill = 10

    [team_service.create(team, np.random.randint(min_skill, max_skill), True) for team in all_teams]


def setup_series_rules(rules):
    config_service.create_best_of_series_rules("Best of 7", 4, rules.oid, [0, 0, 1, 1, 0, 1, 0])


def setup_configuration():
    session = Database.get_session()

    competition_config = CompetitionConfiguration("League", [], [], 1, 1, None)

    table_config = TableSubCompetitionConfiguration("Premier", competition_config, [], [], 1, 1, None)

    competition_config.sub_competitions.append(table_config)

    premier_config = RankingGroupConfiguration("Premier", table_config, None, 1, 1, None)
    western_config = RankingGroupConfiguration("Div A", table_config, premier_config, 2, 1, None)
    eastern_config = RankingGroupConfiguration("Div B", table_config, premier_config, 2, 1, None)

    all = team_service.get_all(session)
    western = []
    eastern = []
    for name in western_teams:
        western.append(team_service.get_team_by_name(name, session))

    for name in eastern_teams:
        eastern.append(team_service.get_team_by_name(name, session))

    team_group_map = {
        western_config.name: {"config": western_config, "teams": western_teams, "sub_comp": table_config},
        eastern_config.name: {"config": eastern_config, "teams": eastern_teams, "sub_comp": table_config},
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
    playoff_config = PlayoffSubCompetitionConfiguration("Playoff", competition_config, [], [], [], 2, 1, None)
    competition_config.sub_competitions.append(playoff_config)

    champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
    runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)

    playoff_config.competition_groups = [champion, runner_up]

    final = SeriesConfiguration("R1S1", 1, playoff_config, western_config, 1, eastern_config, 2, series_rules,
                               champion, premier_config, runner_up, premier_config, 1, None)

    session.commit()



# main scripts
if setup:
    Database.clean_up_database(Database.get_session())
    setup()
