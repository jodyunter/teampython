from teams.data.database import Creation, Database, ClearData

from teams.services.record_service import RecordService
from teams.services.team_service import TeamService

Creation.init_db("sqlite:///:memory:")

team_name_list = ["Toronto", "Montreal", "Calgary", "Edmonton", "Vancouver", "Winnipeg", "Ottawa"]

team_service = TeamService()
record_service = RecordService()

[team_service.create(n, 0) for n in team_name_list]
record_service.add(team_service.get_all(), 5)

for t in list(team_service.get_all()):
    print(t.name)

records = list(record_service.get_by_year(5))

for r in records:
    print(r.team_name + " " + str(r.points))
    r.wins += 5

record_service.update_records(records)

records = list(record_service.get_by_year(5))

for r in records:
    print(r.team_name + " " + str(r.points))

