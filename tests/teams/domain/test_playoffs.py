from unittest import TestCase

from teams.domain.game import Game
from teams.domain.playoff import PlayoffSeries, PlayoffSeriesRules
from teams.domain.team import Team


class TestPlayoffSeries(TestCase):

    def test_process_game_home_win(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 4, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        self.assertFalse(ps.check_complete())

        g1 = Game(1, 1, ht, at, 5, 0, True, False, None, "B")
        ps.process_game(g1)
        self.assertEqual(1, ps.team1_wins)
        self.assertFalse(0, ps.team2_wins)

        g2 = Game(1, 2, ht, at, 5, 0, True, False, None, "A")
        ps.process_game(g2)
        self.assertEqual(2, ps.team1_wins)
        self.assertFalse(0, ps.team2_wins)

        g3 = Game(1, 3, ht, at, 5, 6, True, False, None, "A")
        ps.process_game(g3)
        self.assertEqual(2, ps.team1_wins)
        self.assertFalse(1, ps.team2_wins)

