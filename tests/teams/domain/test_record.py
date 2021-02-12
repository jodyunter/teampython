from unittest import TestCase

from teams.domain.record import Record
from teams.domain.team import Team


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

    def test_sort_records_default(self):
        r1 = Record(-1, Team("Team 1", 5, False), 255, 10, 0, 0, 0, 0, 0, "")
        r2 = Record(-1, Team("Team 2", 5, False), 255, 9, 0, 2, 0, 0, 0, "")
        r3 = Record(-1, Team("Team 3", 5, False), 255, 6, 2, 2, 0, 0, 0, "")
        r4 = Record(-1, Team("Team 4", 5, False), 255, 7, 3, 0, 0, 0, 0, "")
        r5 = Record(-1, Team("Team 5", 5, False), 255, 0, 0, 4, 12, 12, 0, "")
        r6 = Record(-1, Team("Team 6", 5, False), 255, 0, 0, 4, 6, 12, 0, "")
        r7 = Record(-1, Team("Team 7", 5, False), 255, 0, 0, 4, 12, 6, 0, "")

        records = [r7, r5, r6, r1, r2, r4, r3]

        Record.sort_records_default(records)

        self.assertEqual(1, records[0].rank)
        self.assertEqual(2, records[1].rank)
        self.assertEqual(3, records[2].rank)
        self.assertEqual(4, records[3].rank)
        self.assertEqual(5, records[4].rank)
        self.assertEqual(6, records[5].rank)
        self.assertEqual(7, records[6].rank)

        self.assertEqual("Team 1", records[0].team.name)
        self.assertEqual("Team 2", records[1].team.name)
        self.assertEqual("Team 4", records[2].team.name)
        self.assertEqual("Team 3", records[3].team.name)
        self.assertEqual("Team 7", records[4].team.name)
        self.assertEqual("Team 5", records[5].team.name)
        self.assertEqual("Team 6", records[6].team.name)
