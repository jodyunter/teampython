from unittest import TestCase

from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.team_repository import TeamRepository
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper
from tests.teams.repo.test_repository import TestBaseRepository


class TestTeamRepository(TestBaseRepository, TestCase):
    def test_get_by_name(self):
        name = "team 1 by name"
        session = self.setup_basic_test()
        session.add(TeamDTO(Team(name, 12, True)))
        session.commit()

        dto = TeamRepository.get_by_name(name, session)

        self.assertEqual(name, dto.name)
        self.assertIsNotNone(dto.oid)
        self.assertEqual(12, dto.skill)

    def test_get_all(self):
        session = self.setup_basic_test()

        for i in range(5):
            TeamRepository.add(TeamDTO(Team("team " + str(i) + " add_all", i, True)), TeamDTO, session)

        session.commit()

        dto_list = TeamRepository.get_all(TeamDTO, session)

        self.assertEqual(5, len(dto_list))

    def test_get_by_oid(self):
        session = self.setup_basic_test()

        for i in range(5):
            oid = IDHelper.get_new_id()
            TeamRepository.add(TeamDTO(Team("team " + str(i) + " add_all", i, True, oid)), TeamDTO, session)

        session.commit()

        dto = TeamRepository.get_by_oid(oid, TeamDTO, session)

        self.assertIsNotNone(dto, oid)
        self.assertEqual(dto.oid, oid)

    def should_get_by_status(self):
        session = self.setup_basic_test()

        for i in range(5):
            oid = IDHelper.get_new_id()
            active = True
            if i % 2 == 0:
                active = False
            TeamRepository.add(TeamDTO(Team("team " + str(i) + " add_all", i, True, oid)), TeamDTO, session)

        session.commit()

        result = TeamRepository.get_by_active_status(True)
        self.assertEqual(2, len(result))
        result = TeamRepository.get_by_active_status(True)
        self.assertEqual(3, len(result))


