import random

from teams.ConsoleUI.views.game_view import GameView
from teams.ConsoleUI.views.record_view import RecordView
from teams.data.database import Database
from teams.services.app_service import AppService
from teams.services.game_service import GameService, GameRulesService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService

# Database.create_db("sqlite:///:memory:")
Database.create_db("sqlite:///D:\\Coding\\teampython\\mydb.db")
# Database.create_db("sqlite:///C:\\dev\\python_learning\\team_project\\mydb.db")
# Database.clean_up_database(Database.get_session())
# data_setup.setup()

team_service = TeamService()
game_service = GameService()
record_service = RecordService()
game_rules_service = GameRulesService()
app_service = AppService()
rules = game_rules_service.get_by_name("Season")


game_data = app_service.get_current_data()
if game_data.is_year_finished:
    app_service.go_to_next_year()
    rules = game_rules_service.get_by_name("Season")
    app_service.setup_year(rules)


while not app_service.is_year_complete():
    game_data = app_service.get_current_data()
    print("Playing games on day " + str(game_data.current_day))
    r = random
    app_service.play_and_process_games_for_current_day(r)

    for x in game_service.get_games_for_days(game_data.current_year, game_data.current_day, game_data.current_day):
        print(GameView.get_view_with_day(x))


game_data = app_service.get_current_data()
table = record_service.get_by_year(game_data.current_year)

table.sort(key=lambda rec: (-rec.points, -rec.wins, rec.games, -rec.goal_difference))

print("Year: " + str(game_data.current_year))
print(RecordView.get_table_header())
for r in table:
    print(RecordView.get_table_row(r))


