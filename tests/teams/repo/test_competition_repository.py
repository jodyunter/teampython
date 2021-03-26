from unittest import TestCase

from teams.data.repo.competition_repository import CompetitionRepository
from teams.domain.competition import Competition
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestCompetitionRepository(TestBaseRepository, TestCase):

    def test_add(self):
        session = self.setup_basic_test()
        comp = Competition("Test", 1, None, None, 25, False, True, False, True)
        repo = CompetitionRepository()
        repo.add(comp, session)
        session.commit()

        my_comps = repo.get_all(session)

        new_comp = my_comps[0]
        self.assertEqual(1, len(my_comps))
        self.assertEqual("Test", new_comp.name)
        self.assertEqual(1, new_comp.year)
        self.assertEqual(25, new_comp.current_round)
        self.assertFalse(new_comp.setup)
        self.assertTrue(new_comp.started)
        self.assertFalse(new_comp.finished)
        self.assertTrue(new_comp.post_processed)
