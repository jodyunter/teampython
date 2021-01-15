from teams.services.app_service import AppService
from teams.services.base_service import BaseService
from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from teams.services.view_models.standings_views import StandingsHistoryViewModel, StandingsCurrentViewModel, \
    StandingsTeamHistoryViewModel


class StandingsService(BaseService):

    @staticmethod
    def get_standings_history_view(year):
        record_service = RecordService()
        app_service = AppService()
        current_data = app_service.get_current_data()
        records = record_service.get_by_year(year)
        record_service.sort_default(records)
        seasons = record_service.get_all_seasons_for_dropdown()
        seasons.sort(reverse=True)

        return StandingsHistoryViewModel(current_data, year, records, seasons)

    @staticmethod
    def get_standings_team_history_view(team_id):
        record_service = RecordService()
        app_service = AppService()
        team_service = TeamService()
        team = team_service.get_by_id(team_id)
        teams = team_service.get_all()
        current_data = app_service.get_current_data()
        records = record_service.get_by_team(team_id)
        record_service.sort_by_year(records)

        return StandingsTeamHistoryViewModel(current_data, team.name, records, teams)

    @staticmethod
    def get_current_standings_view():
        record_service = RecordService()
        app_service = AppService()
        current_data = app_service.get_current_data()
        records = record_service.get_by_year(current_data.current_year)
        record_service.sort_default(records)

        return StandingsCurrentViewModel(current_data, records)
