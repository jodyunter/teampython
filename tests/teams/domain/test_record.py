from unittest import TestCase

from teams.domain.record import Record


class TestRecord(TestCase):

    def test_get_points(self):
        record = Record(-1, None, -1, 0, 0, 0, 0, 0, 0, "")

        self.assertEqual(0, record.points)
        record.goals_for = 5
        self.assertEqual(0, record.points)
        record.goals_against = 3
        self.assertEqual(0, record.points)
        record.wins = 12
        self.assertEqual(24, record.points)
        record.loses = 3
        self.assertEqual(24, record.points)
        record.ties = 22
        self.assertEqual(46, record.points)

    def test_get_games(self):
        record = Record(-1, None, -1, 1, 2, 3, 0, 0, 0, "")

        self.assertEqual(6, record.games)

    def test_get_goal_difference(self):
        record = Record(-1, None, -1, 1, 2, 3, 4, 10, 0, "")

        self.assertEqual(-6, record.goal_difference)

    def test_process_game_win(self):
        record = Record(-1, "Me", -1, 0, 0, 0, 0, 0, 0, "")

        record.process_game(5, 2)

        self.assertEqual(1, record.wins)
        self.assertEqual(0, record.loses)
        self.assertEqual(0, record.ties)
        self.assertEqual(5, record.goals_for)
        self.assertEqual(2, record.goals_against)

    def test_process_game_lose(self):
        record = Record(-1, "Me", -1, 0, 0, 0, 0, 0, 0, "")

        record.process_game(5, 12)

        self.assertEqual(0, record.wins)
        self.assertEqual(1, record.loses)
        self.assertEqual(0, record.ties)
        self.assertEqual(5, record.goals_for)
        self.assertEqual(12, record.goals_against)

    def test_process_game_tie(self):
        record = Record(-1, "Me", -1, 0, 0, 0, 0, 0, 0, "")

        record.process_game(2, 2)

        self.assertEqual(0, record.wins)
        self.assertEqual(0, record.loses)
        self.assertEqual(1, record.ties)
        self.assertEqual(2, record.goals_for)
        self.assertEqual(2, record.goals_against)
