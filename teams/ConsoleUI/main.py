from teams.ConsoleUI import data_setup
from teams.ConsoleUI.views.game_view import GameView
from teams.ConsoleUI.views.record_view import RecordView
from teams.data.database import Creation
from teams.services.game_service import GameService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService

Creation.create_db("sqlite:///:memory:")
data_setup.setup()

team_service = TeamService()
game_service = GameService()
record_service = RecordService()

team_list = team_service.get_all()
year = 1

record_service.add(team_list, year)

for a in range(len(team_list) - 1):
    for b in range(len(team_list) - a - 1):
        i = a + b + 1
        gvm = game_service.play_game(team_list[a].oid, team_list[i].oid, year, 15, None)
        game_service.process_game(year, gvm.home_id, gvm.home_score, gvm.away_id, gvm.away_score)
        print(GameView.get_basic_view(gvm))
        gvm = game_service.play_game(team_list[i].oid, team_list[a].oid, year, 15, None)
        game_service.process_game(year, gvm.home_id, gvm.home_score, gvm.away_id, gvm.away_score)
        print(GameView.get_basic_view(gvm))

print(RecordView.get_table_header())
for r in record_service.get_by_year(year):
    print(RecordView.get_table_row(r))


