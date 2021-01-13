from flask import Flask, render_template
from markupsafe import escape

from teams.services.app_service import AppService
from teams.services.record_service import RecordService
from teams.data.database import Database
from teams.services.standings_service import StandingsService
from teams.services.team_service import TeamService

app = Flask(__name__)
Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")


@app.route('/teams')
def show_team_list():
    team_service = TeamService()
    teams = team_service.get_all()

    return render_template('teams/index.html', teams=teams)


@app.route('/standings/<year>')
def get_standings_for_year(year):
    standings_service = StandingsService()
    standings_view = standings_service.get_standings_history_view(year)

    return render_template('teams/standings.html', view=standings_view)


@app.route('/standings')
@app.route('/standings/current')
def get_current_standings():
    standings_service = StandingsService()
    standings_view = standings_service.get_current_standings_view()

    return render_template('teams/current_standings.html', view=standings_view)


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
