from unittest import TestCase

from teams.data.dto.dto_competition import CompetitionDTO
from teams.domain.competition import Competition
from tests.teams.repo.test_repository import TestBaseRepository


class TestCompetitionRepository(TestBaseRepository, TestCase):

    def get_add_record(self):
        return CompetitionDTO(Competition("Comp Name", 1, None, None, 2, False, True, False, True))

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

