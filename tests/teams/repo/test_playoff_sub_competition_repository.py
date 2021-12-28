from unittest import TestCase

from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_playoff_sub_competition import PlayoffSubCompetitionDTO
from teams.domain.competition import Competition
from teams.domain.sub_competition import PlayoffSubCompetition
from tests.teams.repo.test_repository import BaseRepoTests


class PlayoffSubCompetitionRepoTests(BaseRepoTests, TestCase):
    def test_add_record(self):
        BaseRepoTests.test_add_record(self)

    def get_add_record(self):
        return PlayoffSubCompetitionDTO(PlayoffSubCompetition("Table Comp", None,
                                                              CompetitionDTO(Competition("My Comp", 1, None, None, 1, False, False, False, False)),
                                                              None, 3, 5, True, True, True, True))

    def get_updated_record(self, original_record):
        original_record.name = "New Sub Name"
        original_record.order = 25
        original_record.current_round = 12
        original_record.setup = False
        original_record.started = False
        original_record.finished = False
        original_record.post_processed = False
        original_record.competition = CompetitionDTO(Competition("Next Comp", 1, None, None, 1, False, False, False, False))

        return original_record

