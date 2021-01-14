import logging

from flask import Flask, render_template
from markupsafe import escape

from teams.data.database import Database
from teams.log_config import log_format, log_level, log_date_format
from teams.services.app_service import AppService
from teams.services.game_service import GameService
from teams.services.standings_service import StandingsService

app = Flask(__name__)
Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")
#  logging.basicConfig(filename=log_file, filemode='w', format=log_format, level=log_level, datefmt=log_date_format)
logging.basicConfig(format=log_format, level=log_level, datefmt=log_date_format)


@app.route('/standings/<year>')
@app.route('/standings/year/<year>')
def get_standings_for_year(year):
    standings_service = StandingsService()
    standings_view = standings_service.get_standings_history_view(year)
    return render_template('standings/pages/historic_year_standings.html', view=standings_view)


@app.route('/standings/team/<team_id>')
def get_standings_for_team(team_id):
    standings_service = StandingsService()
    standings_view = standings_service.get_standings_team_history_view(team_id)

    return render_template('standings/pages/historic_team_standings.html', view=standings_view)


@app.route('/standings')
@app.route('/standings/current')
def get_current_standings():
    standings_service = StandingsService()
    standings_view = standings_service.get_current_standings_view()

    return render_template('standings/pages/current_standings.html', view=standings_view)


@app.route('/games/today')
def get_games_for_today():
    app_service = AppService()
    current_data = app_service.get_current_data()

    game_service = GameService()
    games = game_service.get_games_for_days(current_data.current_year, current_data.current_day, current_data.current_day)

    return render_template('games/pages/game_day.html', current_data=current_data, games=games)
