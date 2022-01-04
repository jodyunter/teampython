from unittest import TestCase

from teams.services.record_service import RecordService
from teams.services.team_service import TeamService
from tests.teams.services.test_team_service import BaseTestService


class TestRecordService(BaseTestService, TestCase):
    team_service = TeamService()
    service = RecordService()

    def test_create(self):
        pass

    def test_get_all(self):
        pass

    def test_add_get_by_year_get_by_team(self):
        self.setup_test()

        for i in range(10):
            self.team_service.create("Team " + str(i), 5, True)

        teams = self.team_service.get_all()

        [self.service.add(self.team_service.get_all(), 25)]
        [self.service.add(self.team_service.get_all(), 35)]
        [self.service.add(self.team_service.get_all(), 2)]

        result = self.service.get_by_year(35)
        [self.assertEqual(35, r.year) for r in result]

        result = self.service.get_by_team_and_year(teams[6].oid, 35)
        self.assertEqual(teams[6].oid, result.team_id, "by year and team")
        self.assertEqual(35, result.year, "by year and team")

    def test_get_by_year(self):
        self.setup_test()
        team_service = TeamService()
        service = RecordService()

        for i in range(10):
            team_service.create("Team " + str(i), 5, True)

        teams = team_service.get_all()

        [service.add(team_service.get_all(), 25)]
        [service.add(team_service.get_all(), 35)]
        [service.add(team_service.get_all(), 2)]

        self.assertEqual(10, len(service.get_by_year(2)))
