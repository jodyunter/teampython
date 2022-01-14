from teams.data.database import Database
from teams.data.repo.competition_configuration_repository import CompetitionConfigurationRepository, \
    TableSubCompetitionConfigurationRepository, RankingGroupConfigurationRepository, \
    CompetitionTeamConfigurationRepository
from teams.data.repo.competition_repository import CompetitionRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain import CompetitionConfiguration, TableSubCompetitionConfiguration, CompetitionTeamConfiguration
from teams.domain.competition_group_configuration import RankingGroupConfiguration
from teams.domain.team import Team
from teams.services.team_service import TeamService

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
competition_config_repo = CompetitionConfigurationRepository()
table_config_repo = TableSubCompetitionConfigurationRepository()
ranking_group_config_repo = RankingGroupConfigurationRepository()
competition_team_config_repo = CompetitionTeamConfigurationRepository()

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
