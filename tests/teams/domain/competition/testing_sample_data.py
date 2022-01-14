from teams.data.database import Database
from teams.data.repo.competition_configuration_repository import CompetitionConfigurationRepository, \
    TableSubCompetitionConfigurationRepository, RankingGroupConfigurationRepository, \
    CompetitionTeamConfigurationRepository
from teams.data.repo.competition_repository import CompetitionRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain import CompetitionConfiguration, TableSubCompetitionConfiguration, CompetitionTeamConfiguration
from teams.domain.competition_group_configuration import RankingGroupConfiguration
from teams.domain.team import Team

connection = "sqlite:///:memory:"
Database.init_db(connection)
session = Database.get_session()
Database.clean_up_database(session)
session.commit()

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
boston = Team("Boston", 5, True)
new_york = Team("New York", 5, True)
detroit = Team("Detroit", 5, True)
chicago = Team("Chicago", 5, True)
seattle = Team("Seattle", 5, True)
minnesota = Team("Minnesota", 5, True)
colorado = Team("Colorado", 5, True)
san_jose = Team("San Jose", 5, True)
los_angelas = Team("Los Angelas", 5, True)
pittsburgh = Team("Pittsburgh", 5, True)

teams = [toronto, montreal, ottawa, quebec_city, calgary, edmonton, vancouver, winnipeg, victoria, saskatoon,
         hamilton, halifax, boston, new_york, detroit, chicago, seattle, minnesota, colorado, san_jose, los_angelas,
         pittsburgh]
western_teams = [calgary, edmonton, vancouver, winnipeg, victoria, saskatoon, seattle, minnesota, colorado, san_jose,
                 los_angelas]
eastern_teams = [toronto, montreal, ottawa, quebec_city, hamilton, halifax, boston, new_york, detroit, chicago,
                 pittsburgh]
pacific_teams = [vancouver, victoria, seattle, san_jose, colorado, los_angelas]
central_teams = [edmonton, calgary, winnipeg, saskatoon, minnesota]
atlantic_teams = [montreal, quebec_city, halifax, boston, new_york, pittsburgh]
north_teams = [toronto, ottawa, hamilton, detroit, chicago]

team_repo = TeamRepository()
competition_config_repo = CompetitionConfigurationRepository()
table_config_repo = TableSubCompetitionConfigurationRepository()
ranking_group_config_repo = RankingGroupConfigurationRepository()
competition_team_config_repo = CompetitionTeamConfigurationRepository()

# create all the teams
[team_repo.add(team, session) for team in teams]
session.commit()

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
 for team in teams]
session.commit()
