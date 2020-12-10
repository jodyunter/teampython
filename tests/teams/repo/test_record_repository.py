import uuid
from unittest import TestCase

from teams.data.dto.dto_record import RecordDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.record_repository import RecordRepository
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestRecordRepository(TestBaseRepository, TestCase):
    repo = RecordRepository()

    def test_add_new_team(self):
        session = self.setup_basic_test()
        team_id = str(uuid.uuid4())
        team_dto = TeamDTO("Record Add For New Team", 5, team_id)

        record_dto = RecordDTO(team_dto, 1, 2, 3, 4, 5, 6, str(uuid.uuid4()))

        self.repo.add(record_dto, session)

        session.commit()

        result = self.repo.get_by_oid(record_dto.oid, session)
        self.assertEqual(result.oid, record_dto.oid)
        self.assertEqual(result.team.oid, record_dto.team.oid)

    def test_add_existing_team(self):
        session = self.setup_basic_test()
        team_id = str(uuid.uuid4())
        team_dto = TeamDTO("Record Add Existing Team", 5, team_id)
        session.add(team_dto)
        session.commit()

        record_dto = RecordDTO(team_dto, 1, 2, 3, 4, 5, 6, str(uuid.uuid4()))

        self.repo.add(record_dto, session)

        session.commit()

        result = self.repo.get_by_oid(record_dto.oid, session)
        self.assertEqual(result.oid, record_dto.oid)
        self.assertEqual(result.team.oid, record_dto.team.oid)

    def test_get_all(self):
        raise NotImplementedError

    @staticmethod
    def create_id():
        return str(uuid.uuid4())

    def test_get_by_year(self):
        session = self.setup_basic_test()
        repo = RecordRepository()
        team_list = []
        for i in range(10):
            new_id = str(uuid.uuid4())
            team_list.append(TeamDTO("GBYN " + str(i), i, new_id))

        team_list = [session.add(t) for t in team_list]

        record_year_30 = [
            repo.add(RecordDTO(team_list[0], 30, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[1], 30, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[2], 30, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_31 = [
            repo.add(RecordDTO(team_list[2], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[4], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[6], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[8], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[9], 31, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_32 = [
            repo.add(RecordDTO(team_list[5], 32, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(RecordDTO(team_list[3], 32, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_33 = [
            repo.add(RecordDTO(team_list[1], 33, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        session.commit()

        self.assertEqual(0, len(list(self.repo.get_by_year(325, session))))
        self.assertEqual(3, len(list(self.repo.get_by_year(30, session))))
        self.assertEqual(5, len(list(self.repo.get_by_year(31, session))))
        self.assertEqual(2, len(list(self.repo.get_by_year(32, session))))
        self.assertEqual(1, len(list(self.repo.get_by_year(33, session))))
