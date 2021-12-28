from unittest import TestCase

from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.team_repository import TeamRepository
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper
from tests.teams.repo.test_repository import BaseRepoTests


class TeamRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return TeamRepository()

    def test_update_record(self):
        BaseRepoTests.test_update_record(self)

    def get_add_record(self):
        return TeamDTO(Team("team 1", 12, True))

    def get_updated_record(self, original_record):
        original_record.name = "Updated Name"
        original_record.skill = "55"
        original_record.active = False
        return original_record

    def test_get_by_name(self):
        session = self.setup_basic_test()
        team = self.get_add_record()
        team.name = "test Name"
        self.get_repo().add(team, session)
        session.commit()

        dto = self.get_repo().get_by_name("test Name", session)

        self.assertEqual(team, dto)

    def test_get_all(self):
        session = self.setup_basic_test()

        for i in range(5):
            self.get_repo().add(TeamDTO(Team("team " + str(i) + " add_all", i, True)), session)

        session.commit()

        dto_list = self.get_repo().get_all(session)

        self.assertEqual(5, len(dto_list))

    def test_get_by_oid(self):
        session = self.setup_basic_test()

        for i in range(5):
            oid = IDHelper.get_new_id()
            self.get_repo().add(TeamDTO(Team("team " + str(i) + " add_all", i, True, oid)), session)

        session.commit()

        dto = self.get_repo().get_by_oid(oid, session)

        self.assertIsNotNone(dto, oid)
        self.assertEqual(dto.oid, oid)

    def should_get_by_status(self):
        session = self.setup_basic_test()

        for i in range(5):
            oid = IDHelper.get_new_id()
            active = True
            if i % 2 == 0:
                active = False
            self.get_repo().add(TeamDTO(Team("team " + str(i) + " add_all", i, True, oid)), session)

        session.commit()

        result = self.get_repo().get_by_active_status(True)
        self.assertEqual(2, len(result))
        result = self.get_repo().get_by_active_status(True)
        self.assertEqual(3, len(result))


