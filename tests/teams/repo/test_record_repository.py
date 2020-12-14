import uuid
from unittest import TestCase

from teams.data.database import Database
from teams.data.dto.dto_record import RecordDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.domain.team import Team
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestRecordRepository(TestBaseRepository, TestCase):
    repo = RecordRepository()

    def test_add_new_team(self):
        session = self.setup_basic_test()
        team_id = str(uuid.uuid4())
        team = Team("Record Add For New Team", 5, team_id)

        record = Record(team, 1, 2, 3, 4, 5, 6, str(uuid.uuid4()))

        self.repo.add(record, session)

        session.commit()

        result = self.repo.get_by_oid(record.oid, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_add_existing_team(self):
        session = self.setup_basic_test()
        team_id = str(uuid.uuid4())
        team = Team("Record Add Existing Team", 5, team_id)
        team_repo = TeamRepository()
        team_repo.add(team, session)
        session.commit()

        team = team_repo.get_by_oid(team.oid, session)
        record = Record(team, 1, 2, 3, 4, 5, 6, str(uuid.uuid4()))

        self.repo.add(record, session)

        session.commit()

        result = self.repo.get_by_oid(record.oid, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_get_all(self):
        session = self.setup_basic_test()
        team_names = ["Team A1", "Team A2", "Team A5"]
        team_repo = TeamRepository()
        [team_repo.add(Team(t, 0, str(uuid.uuid4())), session) for t in team_names]
        session.commit()

        [self.repo.add(Record(team, 1, 2, 3, 4, 5, 6, str(uuid.uuid4())), session)
         for team in team_repo.get_all(session)]
        session.commit()

        self.assertEqual(3, len(self.repo.get_all(session)))



    @staticmethod
    def create_id():
        return str(uuid.uuid4())

    def test_get_by_year(self):
        session = self.setup_basic_test()
        repo = RecordRepository()
        team_repo = TeamRepository()
        self.setup_record_query_data(session, repo, team_repo)

        self.assertEqual(0, len(list(self.repo.get_by_year(325, session))))
        self.assertEqual(3, len(list(self.repo.get_by_year(30, session))))
        self.assertEqual(5, len(list(self.repo.get_by_year(31, session))))
        self.assertEqual(2, len(list(self.repo.get_by_year(32, session))))
        self.assertEqual(1, len(list(self.repo.get_by_year(33, session))))

    def setup_record_query_data(self, session, repo, team_repo):
        team_list = []
        for i in range(10):
            new_id = str(uuid.uuid4())
            team_list.append(Team("GBYN " + str(i), i, new_id))

        [team_repo.add(t, session) for t in team_list]
        # need them to be DTOs!
        team_list = team_repo.get_all(session)

        record_year_30 = [
            repo.add(Record(team_list[0], 30, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[1], 30, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[2], 30, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_31 = [
            repo.add(Record(team_list[2], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[4], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[6], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[8], 31, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[9], 31, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_32 = [
            repo.add(Record(team_list[5], 32, 0, 0, 0, 0, 0, self.create_id()), session),
            repo.add(Record(team_list[3], 32, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        record_year_33 = [
            repo.add(Record(team_list[1], 33, 0, 0, 0, 0, 0, self.create_id()), session),
        ]

        session.commit()

    def test_get_by_team_and_year(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)

        repo = RecordRepository()
        team_repo = TeamRepository()
        self.setup_record_query_data(session, repo, team_repo)

        team = team_repo.get_by_name("GBYN 1", session)

        result = repo.get_by_team_and_year(team.oid, 30, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 30)

        result = repo.get_by_team_and_year(team.oid, 33, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 33)