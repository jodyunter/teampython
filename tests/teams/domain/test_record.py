from unittest import TestCase

from teams.domain.record import Record


class TestRecord(TestCase):

    def test_get_points(self):
        record = Record(None, -1, 0, 0, 0, 0, 0)

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
        raise NotImplementedError

    def test_get_goal_difference(self):
        raise NotImplementedError
