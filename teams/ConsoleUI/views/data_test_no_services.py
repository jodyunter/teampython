from teams.data.database import Database
from teams.data.repo.game_data_repository import GameDataRepository
from teams.data.repo.rules_repository import GameRulesRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain import GameData, Team, GameRules


# setup database
Database.init_db("sqlite:///:memory:")
session = Database.get_session()
Database.clean_up_database(session)

# initialize repositories
game_data_repo = GameDataRepository()
team_repo = TeamRepository()
game_rules_repo = GameRulesRepository()

# setup game data
game_data_repo.add(GameData("Start", 1, 1, False, False), session)
session.commit()

# setup teams
team_names = ["Calgary", "Edmonton", "Vancouver", "Victoria"]
teams = []
for n in team_names:
    teams.append(team_repo.add(Team(n, 5, True), session))
session.commit()

# setup game rules
game_rules_list = [
    GameRules("Season Game Rules", True),
    GameRules("Playoff Game Rules", False)
]
for gr in game_rules_list:
    game_data_repo.add(gr, session)
session.commit()


# get the current game data
game_data = game_data_repo.get_current_data(session)

print("Year: " + str(game_data.current_year))
print("Day: " + str(game_data.current_day))
