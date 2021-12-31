from unittest import TestCase

from teams.data.repo.competition_repository import CompetitionRepository, PlayoffSubCompetitionRepository, \
    TableSubCompetitionRepository
from teams.domain.competition import Competition
from teams.domain.sub_competition import PlayoffSubCompetition, TableSubCompetition
from tests.teams.repo.test_repository import BaseRepoTests


class CompetitionRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return CompetitionRepository()

    def get_add_record(self):
        return Competition("Comp Name", 1, None, None, 2, False, True, False, True)

    def get_updated_record(self, original_record):
        original_record.name = "New Comp Name"
        original_record.year = 10
        original_record.sub_competitions = None
        original_record.teams = None
        original_record.current_round = 3
        original_record.setup = True
        original_record.finished = False
        original_record.processed = True
        original_record.post_processed = False

        return original_record


class TableSubCompetitionRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return TableSubCompetitionRepository()

    def get_add_record(self):
        return TableSubCompetition("Table Comp", None,
                                   Competition("My Comp", 1, None, None, 1, False, False, False, False),
                                   None, 3, True, True, False, False)

    def get_updated_record(self, original_record):
        original_record.name = "New Sub Name"
        original_record.order = 25
        original_record.setup = False
        original_record.started = False
        original_record.finished = False
        original_record.post_processed = False
        original_record.competition = Competition("Next Comp", 1, None, None, 1, False, False, False, False)

        return original_record


class PlayoffSubCompetitionRepoTests(BaseRepoTests, TestCase):
    def get_repo(self):
        return PlayoffSubCompetitionRepository()

    def test_add_record(self):
        BaseRepoTests.test_add_record(self)

    def get_add_record(self):
        return PlayoffSubCompetition("Table Comp", None,
                                     Competition("My Comp", 1, None, None, 1, False, False, False, False),
                                     None, 3, 5, True, True, True, True)

    def get_updated_record(self, original_record):
        original_record.name = "New Sub Name"
        original_record.order = 25
        original_record.current_round = 12
        original_record.setup = False
        original_record.started = False
        original_record.finished = False
        original_record.post_processed = False
        original_record.competition = Competition("Next Comp", 1, None, None, 1, False, False, False, False)

        return original_record
