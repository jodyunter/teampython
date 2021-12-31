from unittest import TestCase

from teams.data.database import Database
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper
from tests.teams.repo.test_repository import BaseRepoTests


class RecordRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return RecordRepository()

    def get_team_repo(self):
        return TeamRepository()

    def test_add_record(self):
        BaseRepoTests.test_add_record(self)

    def test_updated_record(self):
        BaseRepoTests.test_update_record(self)

    def get_add_record(self):
        return Record(5, Team("Team Name", 5, True), 25, 10, 20, 30, 40, 50, 200)

    def get_updated_record(self, original_record):
        original_record.rank = 3
        original_record.year = 15
        original_record.wins = 1
        original_record.loses = 2
        original_record.ties = 3
        original_record.goals_for = 4
        original_record.goals_against = 5
        original_record.skill = 20
        original_record.team = Team("New Team Name", 12, False)

        return original_record

    def test_add_new_team(self):
        session = self.setup_basic_test()
        team_id = IDHelper.get_new_id()
        team = Team("Record Add For New Team", 5, True, team_id)

        record = Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id())

        self.get_repo().add(record, session)

        session.commit()

        result = self.get_repo().get_by_oid(record.oid, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_add_existing_team(self):
        session = self.setup_basic_test()
        team_id = IDHelper.get_new_id()
        team = Team("Record Add Existing Team", 5, True, team_id)
        self.get_team_repo().add(team, session)
        session.commit()

        team = self.get_team_repo().get_by_oid(team.oid, session)
        record = Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id())

        self.get_repo().add(record, session)

        session.commit()

        result = self.get_repo().get_by_oid(record.oid, session)
        self.assertEqual(result.oid, record.oid)
        self.assertEqual(result.team.oid, record.team.oid)

    def test_get_all(self):
        session = self.setup_basic_test()
        team_names = ["Team A1", "Team A2", "Team A5"]

        [self.get_team_repo().add(Team(t, 0, True, IDHelper.get_new_id()), session) for t in team_names]
        session.commit()

        [self.get_repo().add(Record(1, team, 1, 2, 3, 4, 5, 6, 7, IDHelper.get_new_id()), session)
         for team in self.get_team_repo().get_all(session)]
        session.commit()

        self.assertEqual(3, len(self.get_repo().get_all(session)))

    def test_get_by_year(self):
        session = self.setup_basic_test()
        self.setup_record_query_data(session)

        self.assertEqual(0, len(list(self.get_repo().get_by_year(325, session))))
        self.assertEqual(3, len(list(self.get_repo().get_by_year(30, session))))
        self.assertEqual(5, len(list(self.get_repo().get_by_year(31, session))))
        self.assertEqual(2, len(list(self.get_repo().get_by_year(32, session))))
        self.assertEqual(1, len(list(self.get_repo().get_by_year(33, session))))

    def setup_record_query_data(self, session):
        team_list = []
        for i in range(10):
            new_id = IDHelper.get_new_id()
            team_list.append(Team("GBYN " + str(i), i, True, new_id))

        [self.get_team_repo().add(t, session) for t in team_list]

        team_list = self.get_team_repo().get_all(session)

        record_year_30 = [
            self.get_repo().add(Record(1, team_list[0], 30, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(2, team_list[1], 30, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(3, team_list[2], 30, 0, 0, 0, 0, 0, 0, self.get_id()), session),
        ]

        record_year_31 = [
            self.get_repo().add(Record(1, team_list[2], 31, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(1, team_list[4], 31, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(1, team_list[6], 31, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(1, team_list[8], 31, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(1, team_list[9], 31, 0, 0, 0, 0, 0, 0, self.get_id()), session),
        ]

        record_year_32 = [
            self.get_repo().add(Record(1, team_list[5], 32, 0, 0, 0, 0, 0, 0, self.get_id()), session),
            self.get_repo().add(Record(1, team_list[3], 32, 0, 0, 0, 0, 0, 0, self.get_id()), session),
        ]

        record_year_33 = [
            self.get_repo().add(Record(1, team_list[1], 33, 0, 0, 0, 0, 0, 0, self.get_id()), session),
        ]

        session.commit()

    def test_get_by_team_and_year(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)

        self.setup_record_query_data(session)

        team = self.get_team_repo().get_by_name("GBYN 1", session)

        result = self.get_repo().get_by_team_and_year(team.oid, 30, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 30)

        result = self.get_repo().get_by_team_and_year(team.oid, 33, session)
        self.assertEqual(result.team.oid, team.oid)
        self.assertEqual(result.year, 33)

    def test_get_season_list(self):
        session = self.setup_basic_test()
        self.setup_record_query_data(session)

        count = [a.year for a in self.get_repo().get_list_of_seasons(session)]
        self.assertEqual(4, len(count))
        self.assertEqual(count[0], 30)
        self.assertEqual(count[1], 31)
        self.assertEqual(count[2], 32)
        self.assertEqual(count[3], 33)
