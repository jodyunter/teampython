import uuid
from unittest import TestCase

from teams.domain.competition import CompetitionTeam, CompetitionGame, Competition, PlayoffSubCompetition
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByWinsRules, SeriesByGoalsRules
from teams.domain.team import Team


class TestSeriesByGoals(TestCase):

    def test_should_process_game(self):
        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        game_rules = GameRules("A", True, uuid.uuid4())
        last_game_rules = GameRules("B", False, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 3, game_rules, last_game_rules)

        series = SeriesByGoals(None, "My Series", 1, None, None, 0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                               True, False, None, uuid.uuid4())

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

        game_rules = GameRules("A", True, uuid.uuid4())
        last_game_rules = GameRules("B", False, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 3, game_rules, last_game_rules)

        series = SeriesByGoals(None, "My Series", 1, home_competition_team, away_competition_team,
                               0, 0, 0, series_rules, None, None, None, None, None, None, None, None, True, False, None, uuid.uuid4())

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5, 1, True, False,
                               None, uuid.uuid4())
        series.process_game(game)
        self.assertEqual(5, series.home_goals)
        self.assertEqual(1, series.away_goals)

        game = CompetitionGame(competition, None, 1, home_competition_team, away_competition_team, 5,15, True, False,
                               None, uuid.uuid4())

        series.process_game(game)
        self.assertEqual(10, series.home_goals)
        self.assertEqual(16, series.away_goals)

    def test_should_get_winner_and_loser(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        game_rules = GameRules("A", True, uuid.uuid4())
        last_game_rules = GameRules("B", False, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 3, game_rules, last_game_rules)

        series = SeriesByGoals(None, "My Series", 1, home_competition_team, away_competition_team,
                               0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                               True, False, None, uuid.uuid4())

        series.home_goals = 6
        series.away_goals = 5
        series.games_played = 1
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.games_played = 2
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.games_played = 3
        self.assertEqual(home_competition_team.oid, series.get_winner().oid)
        self.assertEqual(away_competition_team.oid, series.get_loser().oid)

        series.away_goals = 12
        self.assertEqual(home_competition_team.oid, series.get_loser().oid)
        self.assertEqual(away_competition_team.oid, series.get_winner().oid)

        series.away_goals = 12
        series.home_goals = 12
        series.last_game_winner = away_competition_team
        self.assertEqual(home_competition_team.oid, series.get_loser().oid)
        self.assertEqual(away_competition_team.oid, series.get_winner().oid)

        series.last_game_winner = home_competition_team
        self.assertEqual(home_competition_team.oid, series.get_winner().oid)
        self.assertEqual(away_competition_team.oid, series.get_loser().oid)

    def test_should_get_needed_games(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())
        sub_competition = PlayoffSubCompetition("Playoff A", None, competition, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        game_rules = GameRules("A", True, uuid.uuid4())
        last_game_rules = GameRules("B", False, uuid.uuid4())

        series_rules = SeriesByGoalsRules("My Rules", 5, game_rules, last_game_rules, uuid.uuid4())

        series = SeriesByGoals(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                               0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                               True, False, None, uuid.uuid4())

        new_games = series.get_new_games(0, 0)
        self.assertEqual(5, len(new_games))

        new_games = series.get_new_games(1, 0)
        self.assertEqual(4, len(new_games))

        new_games = series.get_new_games(1, 2)
        self.assertEqual(2, len(new_games))

        new_games = series.get_new_games(3, 2)
        self.assertEqual(0, len(new_games))


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

    def test_should_get_winner_and_loser(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        series_rules = SeriesByWinsRules("My Rules", 2, None)

        series = SeriesByWins(None, "My Series", 1, home_competition_team, away_competition_team,
                              0, 0, series_rules, None, None, None, None, None, None, None, None, None, uuid.uuid4())

        series.home_wins = 1
        series.away_wins = 0
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.away_wins = 1
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.home_wins = 2
        series.away_wins = 1
        self.assertEqual(home_competition_team.oid, series.get_winner().oid)
        self.assertEqual(away_competition_team.oid, series.get_loser().oid)

        series.home_wins = 0
        series.away_wins = 2
        self.assertEqual(home_competition_team.oid, series.get_loser().oid)
        self.assertEqual(away_competition_team.oid, series.get_winner().oid)

    def test_should_get_needed_games(self):
        home_team = Team("Team 1", 5, True, uuid.uuid4())
        away_team = Team("Team 2", 5, True, uuid.uuid4())

        competition = Competition("My Comp", 1, None, True, True, False, False, uuid.uuid4())
        sub_competition = PlayoffSubCompetition("Playoff A", None, competition, True, True, False, False, uuid.uuid4())

        home_competition_team = CompetitionTeam(competition, home_team, uuid.uuid4())
        away_competition_team = CompetitionTeam(competition, away_team, uuid.uuid4())

        game_rules = GameRules("Playoff", False, uuid.uuid4())

        series_rules = SeriesByWinsRules("My Rules", 4, game_rules, None, uuid.uuid4())

        series = SeriesByWins(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                              0, 0, series_rules, None, None, None, None, None, None, None, None,
                              True, False,
                              uuid.uuid4())

        # no team wins, means complete games are ties
        self.assertEqual(4, len(series.get_new_games(0, 0)))
        self.assertEqual(4, len(series.get_new_games(1, 0)))
        self.assertEqual(4, len(series.get_new_games(2, 0)))
        self.assertEqual(4, len(series.get_new_games(6, 0)))

        # now we have potential wins
        self.assertEqual(4, len(series.get_new_games(0, 0)))
        self.assertEqual(3, len(series.get_new_games(0, 1)))
        self.assertEqual(2, len(series.get_new_games(0, 2)))
        self.assertEqual(1, len(series.get_new_games(0, 3)))

        series.home_wins = 1
        self.assertEqual(3, len(series.get_new_games(0, 0)))
        self.assertEqual(2, len(series.get_new_games(0, 1)))
        self.assertEqual(1, len(series.get_new_games(0, 2)))
        self.assertEqual(0, len(series.get_new_games(0, 3)))

        series.away_wins = 2
        self.assertEqual(2, len(series.get_new_games(0, 0)))
        self.assertEqual(1, len(series.get_new_games(0, 1)))
        self.assertEqual(0, len(series.get_new_games(0, 2)))