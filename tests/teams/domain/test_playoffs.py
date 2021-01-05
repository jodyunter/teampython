from unittest import TestCase

from teams.domain.game import Game
from teams.domain.playoff import PlayoffSeries, PlayoffSeriesRules
from teams.domain.team import Team


class TestPlayoffSeries(TestCase):

    def test_process_game_team1_win(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 4, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        g1 = Game(1, 1, ht, at, 5, 0, True, False, None, "B")
        ps.process_game(g1)
        self.assertFalse(ps.check_complete())
        self.assertEqual(1, ps.team1_wins, "Team 1 Win")
        self.assertEqual(0, ps.team2_wins, "Team 2 no wins")
        self.assertEqual(1, len(ps.games), "Total games in list")

        g2 = Game(1, 2, ht, at, 15, 6, True, True, None, "A")
        ps.process_game(g2)  # already processed so shouldn't be added
        self.assertFalse(ps.check_complete())
        self.assertEqual(1, ps.team1_wins, "Team 1 Wins second game")
        self.assertEqual(0, ps.team2_wins, "Team 2 wins second game")
        self.assertEqual(2, len(ps.games), "Games in list")

    def test_process_game_team2_win(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 4, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        g1 = Game(1, 1, ht, at, 5, 12, True, False, None, "B")
        ps.process_game(g1)
        self.assertFalse(ps.check_complete())
        self.assertEqual(0, ps.team1_wins)
        self.assertEqual(1, ps.team2_wins)

        g2 = Game(1, 2, ht, at, 15, 55, True, True, None, "A")
        ps.process_game(g2)  # already processed so shouldn't be added
        self.assertFalse(ps.check_complete())
        self.assertEqual(0, ps.team1_wins)
        self.assertEqual(1, ps.team2_wins)

    def test_check_complete(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 2, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        ps.team1_wins = 0
        ps.team2_wins = 0
        self.assertFalse(ps.check_complete())

        ps.team1_wins = 1
        ps.team2_wins = 0
        self.assertFalse(ps.check_complete())

        ps.team1_wins = 1
        ps.team2_wins = 1
        self.assertFalse(ps.check_complete())

        ps.team1_wins = 2
        ps.team2_wins = 1
        self.assertTrue(ps.check_complete())

        ps.team1_wins = 1
        ps.team2_wins = 2
        self.assertTrue(ps.check_complete())

    def test_get_wins_for_team_zero_games(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 2, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        self.assertEqual(0, ps.get_wins_for_team(ps.team1))
        self.assertEqual(0, ps.get_wins_for_team(ps.team2))

    def test_get_wins_for_team_zero_wins_with_games(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 2, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        ps.games.append(Game(1, 5, at, ht, 5, 0, True, True, None, "A"))
        self.assertEqual(0, ps.get_wins_for_team(ps.team1))
        self.assertEqual(1, ps.get_wins_for_team(ps.team2))

    def test_get_wins_for_each_team_lots_of_games(self):
        ht = Team("Team 1", 5, "A")
        at = Team("Team 2", 5, "B")
        psr = PlayoffSeriesRules(1, 2, None, None, None, None, None, None, None)
        ps = PlayoffSeries(1, ht, at, 0, 0, psr, [], True, False)

        ps.games.append(Game(1, 5, at, ht, 5, 0, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 0, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 0, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))
        ps.games.append(Game(1, 5, at, ht, 5, 6, True, True, None, "A"))

        self.assertEqual(7, ps.get_wins_for_team(ps.team1))
        self.assertEqual(3, ps.get_wins_for_team(ps.team2))
