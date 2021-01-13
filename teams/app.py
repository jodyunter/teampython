from flask import Flask, render_template
from markupsafe import escape

from teams.services.record_service import RecordService
from teams.data.database import Database
from teams.services.team_service import TeamService

app = Flask(__name__)
Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")


@app.route('/teams')
def show_team_list():
    team_service = TeamService()
    teams = team_service.get_all()

    return render_template('teams/index.html', teams=teams)


@app.route('/standings')
@app.route('/standings/<year>')
def get_standings_for_year(year=-1):
    record_service = RecordService()

    seasons = record_service.get_all_seasons_for_dropdown()
    seasons.sort(reverse=True)
    if int(year) < 0:
        year = max(seasons)

    records = record_service.get_by_year(year)
    record_service.sort_default(records)

    return render_template('teams/standings.html', records=records, seasons=seasons, current_year=year)


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
