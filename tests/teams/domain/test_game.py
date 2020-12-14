import random
from unittest import TestCase

from teams.domain.game import Game, GameRules


class TestGame(TestCase):

    def test_play(self):
        game = Game(5, 25, None, None, 0, 0, False, False, GameRules("Rules", True, ""), "")

        r = random
        r.seed(1235)

        game.play(r)

        self.assertTrue(game.complete)
