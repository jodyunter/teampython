from unittest import TestCase

from teams.data.database import Database
from teams.data.dto.dto_record import RecordDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.repository import Repository
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper
from tests.teams.repo.test_repository import TestBaseRepository


class TestRecordRepository(TestBaseRepository, TestCase):

    def test_add_record(self):
        TestBaseRepository.test_add_record(self)

    def test_updated_record(self):
        TestBaseRepository.test_update_record(self)

    def get_add_record(self):
        return RecordDTO(Record(5, TeamDTO(Team("Team Name", 5, True)), 25, 10, 20, 30, 40, 50, 200))

    def get_updated_record(self, original_record):
        original_record.rank = 3
        original_record.year = 15
        original_record.wins = 1
        original_record.loses = 2
        original_record.ties = 3
        original_record.goals_for = 4
        original_record.goals_against = 5
        original_record.skill = 20
        original_record.team = TeamDTO(Team("New Team Name", 12, False))

        return original_record

    def test_add_new_team(self):
        session = self.setup_basic_test()
        team_id = IDHelper.get_new_id()
        team = Team("Record Add For New Team", 5, True, team_id)

        record = Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id())

        RecordRepository.add(record, RecordDTO, session)

        session.commit()

        result = RecordRepository.get_by_oid(record.oid, RecordDTO, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_add_existing_team(self):
        session = self.setup_basic_test()
        team_id = IDHelper.get_new_id()
        team = Team("Record Add Existing Team", 5, True, team_id)
        TeamRepository.add(team, TeamDTO, session)
        session.commit()

        team = TeamRepository.get_by_oid(team.oid, TeamDTO, session)
        record = Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id())

        RecordRepository.add(record, RecordDTO, session)

        session.commit()

        result = RecordRepository.get_by_oid(record.oid, RecordDTO, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_get_all(self):
        session = self.setup_basic_test()
        team_names = ["Team A1", "Team A2", "Team A5"]

        [TeamRepository.add(Team(t, 0, True, IDHelper.get_new_id()), TeamDTO, session) for t in team_names]
        session.commit()

        [RecordRepository.add(Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id()), RecordDTO, session)
         for team in TeamRepository.get_all(TeamDTO, session)]
        session.commit()

        self.assertEqual(3, len(RecordRepository.get_all(RecordDTO, session)))

    def test_get_by_year(self):
        session = self.setup_basic_test()
        self.setup_record_query_data(session)

        self.assertEqual(0, len(list(RecordRepository.get_by_year(325, session))))
        self.assertEqual(3, len(list(RecordRepository.get_by_year(30, session))))
        self.assertEqual(5, len(list(RecordRepository.get_by_year(31, session))))
        self.assertEqual(2, len(list(RecordRepository.get_by_year(32, session))))
        self.assertEqual(1, len(list(RecordRepository.get_by_year(33, session))))

    def setup_record_query_data(self, session):
        team_list = []
        for i in range(10):
            new_id = IDHelper.get_new_id()
            team_list.append(Team("GBYN " + str(i), i, True, new_id))

        [Repository.add(t, TeamDTO, session) for t in team_list]
        # need them to be DTOs!
        team_list = Repository.get_all(TeamDTO, session)

        record_year_30 = [
            Repository.add(Record(1, team_list[0], 30, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(2, team_list[1], 30, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(3, team_list[2], 30, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
        ]

        record_year_31 = [
            Repository.add(Record(1, team_list[2], 31, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(1, team_list[4], 31, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(1, team_list[6], 31, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(1, team_list[8], 31, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(1, team_list[9], 31, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
        ]

        record_year_32 = [
            Repository.add(Record(1, team_list[5], 32, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
            Repository.add(Record(1, team_list[3], 32, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
        ]

        record_year_33 = [
            Repository.add(Record(1, team_list[1], 33, 0, 0, 0, 0, 0, 0, self.get_id()), RecordDTO, session),
        ]

        session.commit()

    def test_get_by_team_and_year(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)

        self.setup_record_query_data(session)

        team = TeamRepository.get_by_name("GBYN 1", session)

        result = RecordRepository.get_by_team_and_year(team.oid, 30, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 30)

        result = RecordRepository.get_by_team_and_year(team.oid, 33, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 33)

    def test_get_season_list(self):
        session = self.setup_basic_test()
        self.setup_record_query_data(session)

        count = [a.year for a in RecordRepository.get_list_of_seasons(session)]
        self.assertEqual(4, len(count))
        self.assertEqual(count[0], 30)
        self.assertEqual(count[1], 31)
        self.assertEqual(count[2], 32)
        self.assertEqual(count[3], 33)
