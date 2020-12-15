import random
from unittest import TestCase

from teams.domain.game import Game, GameRules
from teams.domain.team import Team


class TestGame(TestCase):

    def test_play(self):
        game = Game(5, 25, Team("T1", 5, "1"), Team("T1", 4, "2"), 0, 0, False, False, GameRules("Rules", True, ""), "")

        r = random
        r.seed(1235)

        game.play(r)

        self.assertTrue(game.complete)
