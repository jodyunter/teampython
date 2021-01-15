import logging
import random

from flask import Flask, render_template

from teams.data.database import Database
from teams.log_config import log_format, log_level, log_date_format
from teams.services.app_service import AppService
from teams.services.game_service import GameService, GameRulesService
from teams.services.standings_service import StandingsService
from teams.services.view_models.home_page_view_models import HomePageViewModel, ButtonViewModel

app = Flask(__name__)
Database.init_db("sqlite:///C:\\temp\\sqlite\\Data\\mydb.db")
#  logging.basicConfig(filename=log_file, filemode='w', format=log_format, level=log_level, datefmt=log_date_format)
logging.basicConfig(format=log_format, level=log_level, datefmt=log_date_format)

rounds = 4
do_home_and_away = False
rules_name = "Season"  # other is Playoff


@app.route('/')
def get_home_page():
    standings_service = StandingsService()
    standings_view = standings_service.get_current_standings_view()
    app_service = AppService()
    current_data = app_service.get_current_data()

    year = current_data.current_year
    day = current_data.current_day

    game_service = GameService()
    games = game_service.get_games_for_days(year, day, day)
    yesterday_games = game_service.get_games_for_days(year, day-1, day-1)

    button_view = ButtonViewModel(current_data)
    homepage_view = HomePageViewModel(yesterday_games, games, current_data, standings_view, button_view)

    return render_template("homepage.html", view=homepage_view)


@app.route('/playgames',  methods=['POST'])
def button_play_clicked():
    app_service = AppService()

    r = random
    app_service.play_and_process_games_for_current_day(r)

    return get_home_page()


@app.route('/setupseason',  methods=['POST'])
def button_setup_clicked():
    app_service = AppService()
    game_rules_service = GameRulesService()
    rules = game_rules_service.get_by_name(rules_name)

    game_data = app_service.get_current_data()
    if game_data.is_year_finished:
        app_service.go_to_next_year()
        app_service.setup_year(rules, rounds, do_home_and_away)

    return get_home_page()


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
