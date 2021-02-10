import uuid
from unittest import TestCase

from teams.domain.competition import SeriesByWins, CompetitionTeam, CompetitionGame, Competition, SeriesByGoals
from teams.domain.series_rules import SeriesByWinsRules, SeriesByGoalsRules
from teams.domain.team import Team


class TestSeriesByGoals(TestCase):

    def test_should_process_game(self):
        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 3, None)

        series = SeriesByGoals(None, "My Series", 1, None, None, 0, 0, 0, series_rules, None, None, None, None, None, None, None, None, None, uuid.uuid4())

        game = CompetitionGame(competition, None, 1, None, None, 5, 0, False, False, None, uuid.uuid4())
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        self.assertTrue(series.can_process_game(game))

        game.complete = False
        game.processed = True
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = True
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.games_played = 0
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.games_played = 1
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.games_played = 2
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.games_played = 3
        self.assertFalse(series.can_process_game(game))

    def test_process_game(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 3, None)

        series = SeriesByGoals(None, "My Series", 1, home_competition_team, away_competition_team,
                               0, 0, 0, series_rules, None, None, None, None, None, None, None, None, None, uuid.uuid4())

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5, 1, True, False,
                               None, uuid.uuid4())
        series.process_game(game)
        self.assertEquals(5, series.home_goals)
        self.assertEquals(1, series.away_goals)

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5,15, True, False,
                               None, uuid.uuid4())

        series.process_game(game)
        self.assertEqual(10, series.home_goals)
        self.assertEqual(16, series.away_goals)


class TestSeriesByWins(TestCase):

    def test_should_process_game(self):
        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        series_rules = SeriesByWinsRules("My Rules", 2, None)

        series = SeriesByWins(None, "My Series", 1, None, None, 0, 0, series_rules, None, None, None, None, None, None, None, None, None, uuid.uuid4())

        game = CompetitionGame(competition, None, 1, None, None, 5, 0, False, False, None, uuid.uuid4())
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        self.assertTrue(series.can_process_game(game))

        game.complete = False
        game.processed = True
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = True
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 1
        series.away_wins = 0
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 2
        series.away_wins = 0
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 2
        series.away_wins = 1
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 1
        series.away_wins = 1
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 0
        series.away_wins = 1
        self.assertTrue(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 0
        series.away_wins = 2
        self.assertFalse(series.can_process_game(game))

        game.complete = True
        game.processed = False
        series.home_wins = 1
        series.away_wins = 2
        self.assertFalse(series.can_process_game(game))

    def test_process_game(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        series_rules = SeriesByWinsRules("My Rules", 2, None)

        series = SeriesByWins(None, "My Series", 1, home_competition_team, away_competition_team,
                              0, 0, series_rules, None, None, None, None, None, None, None, None, None, uuid.uuid4())

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5, 0, True, False, None, uuid.uuid4())
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(0, series.away_wins)
        self.assertFalse(series.is_complete())

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5, 6, True, False, None, uuid.uuid4())
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(1, series.away_wins)
        self.assertFalse(series.is_complete())

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5, 6, True, False, None, uuid.uuid4())
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(2, series.away_wins)
        self.assertTrue(series.is_complete())
