from unittest import TestCase

from teams.services.team_service import TeamService
from tests.teams.services.base_test_service import BaseTestService


class TestTeamService(BaseTestService, TestCase):
    service = TeamService()

    def setup_list(self, session=None):
        commit = session is None
        session = self.service.get_session(session)
        team_list = []
        for i in range(10):
            vm = self.service.create("Team " + str(i), i*10, True, session)
            team_list.append(vm)

        self.service.commit(session, commit)

        return team_list

    def test_create(self):
        self.setup_test()
        name = "Creation Team"
        team_view = self.service.create(name, 12, True)

        self.assertEqual(name, team_view.name)
        self.assertEqual(12, team_view.skill)
        self.assertIsNotNone(team_view.oid)

    def test_get_by_name(self):
        self.setup_test()
        team_list = self.setup_list()

        team_5 = self.service.get_by_name("Team 5")

        team_from_list = [team for team in team_list if team.name == "Team 5"][0]

        self.assertEqual(team_5.name, team_from_list.name)
        self.assertEqual(team_5.skill, team_from_list.skill)
        self.assertIsNotNone(team_5.oid, team_from_list.oid)

    def test_get_by_oid(self):
        self.setup_test()
        team_list = self.setup_list()

        team_from_list = [team for team in team_list if team.name == "Team 3"][0]

        team_3 = self.service.get_by_id(team_from_list.oid)

        self.assertEqual(team_3.name, team_from_list.name)
        self.assertEqual(team_3.skill, team_from_list.skill)
        self.assertIsNotNone(team_3.oid, team_from_list.oid)

    def test_create_and_update(self):
        self.setup_test()
        self.service.create("New Team", 55, True)

        view = self.service.get_by_name("New Team")

        self.service.update(view.oid, "Updated Name", 33, False)

        view2 = self.service.get_by_id(view.oid)

        self.assertEqual(view.oid, view2.oid)
        self.assertEqual("Updated Name", view2.name)
        self.assertEqual(33, view2.skill)
        self.assertFalse(view2.active)

    def test_get_all(self):
        self.setup_test()
        current = len(self.service.get_all())
        for k in range(10):
            self.service.create("Team Get All " + str(k), k, True)

        all_data = self.service.get_all()

        self.assertEqual(10 + current, len(all_data))
