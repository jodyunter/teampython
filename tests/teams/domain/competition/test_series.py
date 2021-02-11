import uuid
from unittest import TestCase

from teams.domain.competition import CompetitionTeam, CompetitionGame, Competition, PlayoffSubCompetition, SeriesGame
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals, SeriesByWins
from teams.domain.series_rules import SeriesByWinsRules, SeriesByGoalsRules
from teams.domain.team import Team
from teams.domain.utility.utility_classes import IDHelper


class TestSeriesByGoals(TestCase):

    @staticmethod
    def setup_default_series(games):
        home_team = Team("Team 1", 5, True, IDHelper.get_new_id())
        away_team = Team("Team 2", 5, True, IDHelper.get_new_id())

        competition = Competition("My Comp", 1, None, True, True, False, False, IDHelper.get_new_id())
        sub_competition = PlayoffSubCompetition("Playoff A", None, competition, True, True, False, False,
                                                IDHelper.get_new_id())

        home_competition_team = CompetitionTeam(competition, home_team, IDHelper.get_new_id())
        away_competition_team = CompetitionTeam(competition, away_team, IDHelper.get_new_id())

        game_rules = GameRules("A", True, IDHelper.get_new_id())
        last_game_rules = GameRules("B", False, IDHelper.get_new_id())

        series_rules = SeriesByGoalsRules("My Rules", games, game_rules, last_game_rules, IDHelper.get_new_id())

        series = SeriesByGoals(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                               0, 0, 0, series_rules, None, None, None, None, None, None, None, None,
                               True, False, IDHelper.get_new_id())

        return series

    def test_should_process_game(self):
        series = TestSeriesByGoals.setup_default_series(3)

        game = CompetitionGame(series.sub_competition.competition, None, 1, None, None, 5, 0, False, False, None, IDHelper.get_new_id())
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
        series.home_goals = 0
        series.away_goals = 3
        self.assertFalse(series.can_process_game(game))

        # we can process this game because the series isn't complete, even though the games are played, the goals are tied, we need a last game
        game.complete = True
        game.processed = False
        series.games_played = 3
        series.home_goals = 3
        series.away_goals = 3
        self.assertTrue(series.can_process_game(game))

        # we can process this game because the series isn't complete, even though the games are played, the goals are tied, we need a last game
        game.complete = True
        game.processed = False
        series.games_played = 4
        series.home_goals = 3
        series.away_goals = 3
        self.assertTrue(series.can_process_game(game))

        # we can process this game because the series isn't complete, even though the games are played, the goals are tied, we need a last game
        game.complete = True
        game.processed = False
        series.games_played = 3
        series.home_goals = 4
        series.away_goals = 3
        self.assertFalse(series.can_process_game(game))

    def test_process_game(self):
        series = TestSeriesByGoals.setup_default_series(3)

        game = SeriesGame(series, 1, series.sub_competition.competition, None, 1, series.home_team, series.away_team, 5, 1, True,
                          False, None, IDHelper.get_new_id())
        series.process_game(game)
        self.assertEqual(5, series.home_goals)
        self.assertEqual(1, series.away_goals)

        game = SeriesGame(series, 2, series.sub_competition.competition, None, 1, series.home_team, series.away_team, 5, 15, True, False,
                          None, IDHelper.get_new_id())

        series.process_game(game)
        self.assertEqual(10, series.home_goals)
        self.assertEqual(16, series.away_goals)

    def test_should_get_winner_and_loser(self):
        series = TestSeriesByGoals.setup_default_series(3)

        series.home_goals = 6
        series.away_goals = 5
        series.games_played = 1
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.home_goals = 6
        series.away_goals = 5
        series.games_played = 2
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.home_goals = 6
        series.away_goals = 5
        series.games_played = 3
        self.assertEqual(series.home_team.oid, series.get_winner().oid)
        self.assertEqual(series.away_team.oid, series.get_loser().oid)

        series.home_goals = 6
        series.away_goals = 12
        series.games_played = 3
        self.assertEqual(series.home_team.oid, series.get_loser().oid)
        self.assertEqual(series.away_team.oid, series.get_winner().oid)

        series.away_goals = 12
        series.home_goals = 12
        series.games_played = 3
        self.assertIsNone(series.get_loser())
        self.assertIsNone(series.get_winner())

        series.away_goals = 13
        series.home_goals = 12
        series.games_played = 4
        self.assertEqual(series.home_team.oid, series.get_loser().oid)
        self.assertEqual(series.away_team.oid, series.get_winner().oid)

    def test_should_get_needed_games(self):
        series = TestSeriesByGoals.setup_default_series(5)

        new_games = series.get_new_games(0, 0)
        self.assertEqual(5, len(new_games))

        new_games = series.get_new_games(1, 0)
        self.assertEqual(4, len(new_games))

        new_games = series.get_new_games(1, 2)
        self.assertEqual(2, len(new_games))

        new_games = series.get_new_games(3, 2)
        self.assertEqual(0, len(new_games))

        new_games = series.get_new_games(5, 0)
        self.assertEqual(1, len(new_games))

    def test_create_new_game(self):
        series = TestSeriesByGoals.setup_default_series(2)

        game = series.create_game(2)

        self.assertEqual(2, game.game_number)
        self.assertEqual(series.home_team.oid, game.home_team.oid)
        self.assertEqual(series.away_team.oid, game.away_team.oid)
        self.assertEqual(game.competition.oid, series.sub_competition.competition.oid)
        self.assertEqual(game.sub_competition.oid, series.sub_competition.oid)
        self.assertFalse(game.complete)
        self.assertFalse(game.processed)
        self.assertEqual(-1, game.day)
        self.assertEqual(series.sub_competition.competition.year, game.year)
        self.assertEqual(series.series_rules.game_rules.oid, game.rules.oid)

        game = series.create_game(5)

        self.assertEqual(5, game.game_number)
        self.assertEqual(series.home_team.oid, game.home_team.oid)
        self.assertEqual(series.away_team.oid, game.away_team.oid)
        self.assertEqual(game.competition.oid, series.sub_competition.competition.oid)
        self.assertEqual(game.sub_competition.oid, series.sub_competition.oid)
        self.assertFalse(game.complete)
        self.assertFalse(game.processed)
        self.assertEqual(-1, game.day)
        self.assertEqual(series.sub_competition.competition.year, game.year)
        self.assertEqual(series.series_rules.last_game_rules.oid, game.rules.oid)


class TestSeriesByWins(TestCase):
    @staticmethod
    def create_game(competition, home_team, away_team, home_goals, away_goals, complete=True, processed=False):
        return CompetitionGame(competition, None, 1, home_team, away_team, home_goals, away_goals, complete, processed,
                               None, IDHelper.get_new_id())

    @staticmethod
    def setup_default_series(games):
        home_team = Team("Team 1", 5, True, IDHelper.get_new_id())
        away_team = Team("Team 2", 5, True, IDHelper.get_new_id())

        competition = Competition("My Comp", 1, None, True, True, False, False, IDHelper.get_new_id())
        sub_competition = PlayoffSubCompetition("My Playoff", None, competition, True, False, False, False, IDHelper.get_new_id())

        home_competition_team = CompetitionTeam(competition, home_team, IDHelper.get_new_id())
        away_competition_team = CompetitionTeam(competition, away_team, IDHelper.get_new_id())

        game_rules = GameRules("My Rules", False, IDHelper.get_new_id())

        series_rules = SeriesByWinsRules("My Rules", games, game_rules, None, IDHelper.get_new_id())

        series = SeriesByWins(sub_competition, "My Series", 1, home_competition_team, away_competition_team,
                              0, 0, series_rules, None, None, None, None, None, None, None, None,
                              True, False,
                              IDHelper.get_new_id())

        return series

    def test_should_process_game(self):
        series = TestSeriesByWins.setup_default_series(2)

        game = CompetitionGame(series.sub_competition.competition, None, 1, None, None, 5, 0, False, False, None, IDHelper.get_new_id())
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
        series = TestSeriesByWins.setup_default_series(2)
        competition = series.sub_competition.competition

        game = TestSeriesByWins.create_game(competition, series.home_team, series.away_team, 6, 5)
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(0, series.away_wins)
        self.assertFalse(series.is_complete())

        game = TestSeriesByWins.create_game(competition, series.home_team, series.away_team, 5, 6)
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(1, series.away_wins)
        self.assertFalse(series.is_complete())

        game = TestSeriesByWins.create_game(competition, series.home_team, series.away_team, 5, 6)
        series.process_game(game)
        self.assertEqual(1, series.home_wins)
        self.assertEqual(2, series.away_wins)
        self.assertTrue(series.is_complete())

    def test_should_get_winner_and_loser(self):
        series = TestSeriesByWins.setup_default_series(2)

        series.home_wins = 1
        series.away_wins = 0
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.away_wins = 1
        self.assertIsNone(series.get_winner())
        self.assertIsNone(series.get_loser())

        series.home_wins = 2
        series.away_wins = 1
        self.assertEqual(series.home_team.oid, series.get_winner().oid)
        self.assertEqual(series.away_team.oid, series.get_loser().oid)

        series.home_wins = 0
        series.away_wins = 2
        self.assertEqual(series.home_team.oid, series.get_loser().oid)
        self.assertEqual(series.away_team.oid, series.get_winner().oid)

    def test_should_get_needed_games(self):
        series = TestSeriesByWins.setup_default_series(4)

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

    def test_should_create_new_game(self):
        series = TestSeriesByWins.setup_default_series(4)

        game = series.create_game(5)

        self.assertEqual(5, game.game_number)
        self.assertEqual(series.home_team.oid, game.home_team.oid)
        self.assertEqual(series.away_team.oid, game.away_team.oid)
        self.assertEqual(game.competition.oid, series.sub_competition.competition.oid)
        self.assertEqual(game.sub_competition.oid, series.sub_competition.oid)
        self.assertFalse(game.complete)
        self.assertFalse(game.processed)
        self.assertEqual(-1, game.day)
        self.assertEqual(series.sub_competition.competition.year, game.year)
        self.assertEqual(series.series_rules.game_rules.oid, game.rules.oid)

    def test_home_team_pattern(self):
        raise NotImplementedError
