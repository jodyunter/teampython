from unittest import TestCase

from teams.data.database import Database
from teams.services.team_service import TeamService


class BaseTestService:
    @staticmethod
    def setup_test():
        Database.init_db("sqlite:///:memory:")


class TestTeamService(TestCase):

    def test_create_and_get_by_name_and_get_by_oid(self):
        BaseTestService.setup_test()
        service = TeamService()
        service.create("Team 1 create", 12)
        team_view = service.get_team_by_name("Team 1 create")

        self.assertEqual("Team 1 create", team_view.name)
        self.assertEqual(12, team_view.skill)
        self.assertIsNotNone(team_view.oid)

        team_view2 = service.get_by_id(team_view.oid)

        self.assertEqual(team_view2.oid, team_view.oid)
        self.assertEqual(team_view2.name, team_view.name)
        self.assertEqual(team_view2.skill, team_view.skill)

    def test_create_and_update(self):
        BaseTestService.setup_test()
        service = TeamService()
        service.create("New Team", 55)

        view = service.get_team_by_name("New Team")

        service.update(view.oid, "Updated Name", 33)

        view2 = service.get_by_id(view.oid)

        self.assertEqual(view.oid, view2.oid)
        self.assertEqual("Updated Name", view2.name)
        self.assertEqual(33, view2.skill)

    def test_get_all(self):
        BaseTestService.setup_test()
        service = TeamService()
        current = len(service.get_all())
        for k in range(10):
            service.create("Team Get All " + str(k), k)

        all_data = service.get_all()

        self.assertEqual(10 + current, len(all_data))
