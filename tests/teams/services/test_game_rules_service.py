from unittest import TestCase

from teams.services.game_rules_service import GameRulesService
from tests.teams.services.test_team_service import BaseTestService


class TestGameRulesService(BaseTestService, TestCase):
    service = GameRulesService()

    def setup_list(self, session=None):
        commit = session is None
        session = self.service.get_session()
        self.service.create("Test Rules A", True, session)
        self.service.create("Test Rules B", True, session)
        self.service.create("Test Rules C", True, session)
        self.service.create("Test Rules D", True, session)
        self.service.create("Test Rules E", True, session)
        self.service.commit(session, commit)

    def test_create(self):
        self.setup_test()
        rules_vm = self.service.create("My Rules", True)
        self.assertIsNotNone(rules_vm.oid)
        self.assertEqual("My Rules", rules_vm.name)
        self.assertTrue(rules_vm.can_tie)
        pass

    def test_get_by_name(self):
        self.setup_test()
        self.setup_list()

        rules = self.service.get_by_name("Test Rules D")
        self.assertEqual("Test Rules D", rules.name)

    def test_get_all(self):
        self.setup_test()
        self.setup_list()

        all_rules = self.service.get_all()

        self.assertEqual(5, len(all_rules))
        all_names = [rule.name for rule in all_rules]
        self.assertTrue("Test Rules A" in all_names)
        self.assertTrue("Test Rules B" in all_names)
        self.assertTrue("Test Rules C" in all_names)
        self.assertTrue("Test Rules D" in all_names)
        self.assertTrue("Test Rules E" in all_names)