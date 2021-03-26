import random
from unittest import TestCase

import numpy as np

from teams.ConsoleUI.views.record_view import RecordView
from teams.domain.game import Game, GameRules
from teams.domain.record import Record
from teams.domain.team import Team
from teams.services.record_service import RecordService


class TestGame(TestCase):

    def test_play(self):
        game = Game(5, 25, Team("T1", 5, True, "1"), Team("T1", 4, True, "2"), 0, 0, False, False, GameRules("Rules", True, ""), "")

        np.random.seed = 1235
        game.play()

        self.assertTrue(game.complete)

    def test_stats(self):
        t1_skill = 10
        t2_skill = 0
        team1 = Team("T1", t1_skill, True, "1")
        team2 = Team("T2", t2_skill, True, "2")

        record1 = Record(1, team1, 1, 0, 0, 0, 0, 0, 0, "3")
        record2 = Record(1, team2, 1, 0, 0, 0, 0, 0, 0, "3")

        rules = GameRules("Rules", True, "4")

        for i in range(1000):
            game = Game(1, 1, team1, team2, 0, 0, False, False, rules, str(i))
            game.play()
            record1.process_game(game.home_score, game.away_score)
            record2.process_game(game.away_score, game.home_score)

        print()
        print("Results")
        print(RecordView.get_table_header())
        print(RecordView.get_table_row(RecordService.get_view_from_model(record1)))
        print(RecordView.get_table_row(RecordService.get_view_from_model(record2)))
