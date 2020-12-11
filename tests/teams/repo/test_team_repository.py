import uuid
from unittest import TestCase

from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.team_repository import TeamRepository
from teams.domain.team import Team
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestTeamRepository(TestBaseRepository, TestCase):
    def test_get_by_name(self):
        name = "team 1 by name"
        session = self.setup_basic_test()
        session.add(TeamDTO(Team(name, 12, str(uuid.uuid4()))))
        session.commit()

        repo = TeamRepository()
        dto = repo.get_by_name(name, session)

        self.assertEqual(name, dto.name)
        self.assertIsNotNone(dto.oid)
        self.assertEqual(12, dto.skill)

    def test_get_all(self):
        session = self.setup_basic_test()

        repo = TeamRepository()
        for i in range(5):
            repo.add(TeamDTO(Team("team " + str(i) + " add_all", i, str(uuid.uuid4()))), session)

        session.commit()

        dto_list = repo.get_all(session)

        self.assertEqual(5, len(dto_list))

    def test_get_by_oid(self):
        session = self.setup_basic_test()

        repo = TeamRepository()

        for i in range(5):
            oid = str(uuid.uuid4())
            repo.add(TeamDTO(Team("team " + str(i) + " add_all", i, oid)), session)

        session.commit()

        dto = repo.get_by_oid(oid, session)

        self.assertIsNotNone(dto, oid)
        self.assertEqual(dto.oid, oid)


