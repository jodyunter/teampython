import random

from teams.ConsoleUI import data_setup
from teams.ConsoleUI.views.game_view import GameView
from teams.ConsoleUI.views.record_view import RecordView
from teams.data.database import Database
from teams.domain.game import GameRules
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService

Database.create_db("sqlite:///:memory:")
data_setup.setup()

team_service = TeamService()
game_service = GameService()
record_service = RecordService()

team_list = team_service.get_all()
year = 1

record_service.add(team_list, year)
r = random.SystemRandom()

game_service.create_games(team_service.get_all(), 1, 10, GameRules("Rules", False), True)
game_service.play_game(game_service.get_all_games(), r)
game_service.process_games()

for x in game_service.get_all_games():
    print(GameView.get_basic_view(x))

table = record_service.get_by_year(year)

table.sort(key=lambda x: (-x.points, -x.wins, x.games, -x.goal_difference))

print(RecordView.get_table_header())
for r in table:
    print(RecordView.get_table_row(r))


