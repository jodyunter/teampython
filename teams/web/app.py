from flask import Flask
from markupsafe import escape

from teams.data.database import Database
from teams.services.team_service import TeamService

app = Flask(__name__)

Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")


@app.route('/')
def hello_world():
    team_service = TeamService()
    result = ""
    for t in team_service.get_all():
        result += t.name + "\n"

    return 'Hello World\n' + result


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
