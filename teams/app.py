from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from markupsafe import escape

from teams.services.record_service import RecordService
from teams.data.database import Database
from teams.services.team_service import TeamService

app = Flask(__name__)
Bootstrap(app)
Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")


@app.route('/teams')
def show_team_list():
    team_service = TeamService()
    teams = team_service.get_all()

    return render_template('teams/index.html.j2', teams=teams)

@app.route('/standings/<year>')
def get_standings_for_year(year):
    record_service = RecordService()
    records = record_service.get_by_year(year)
    record_service.sort_default(records)
    return render_template('teams/standings.html.j2', records=records)


@app.route('/newuser')
def show_new_user_Profile():
    return render_template('example.html.j2')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('index.html.j2', user=username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
