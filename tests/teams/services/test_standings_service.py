from unittest import TestCase

from teams.services.app_service import AppService
from teams.services.record_service import RecordService
from teams.services.standings_service import StandingsService
from teams.services.team_service import TeamService
from tests.teams.services.test_team_service import BaseTestService


class TestStandingsService(BaseTestService, TestCase):

    def test_should_get_standings_history_view(self):
        self.setup_test()
        team_service = TeamService()
        record_service = RecordService()
        app_service = AppService()
        app_service.setup_data(35, 1, True, True)

        standings_service = StandingsService()

        for i in range(10):
            team_service.create("Team " + str(i), 5, True)

        [record_service.add(team_service.get_all(), 25)]
        [record_service.add(team_service.get_all(), 35)]
        [record_service.add(team_service.get_all(), 2)]

        result = standings_service.get_standings_history_view(2)
        self.assertEqual(10, len(result.records))
