from unittest import TestCase

from pytest import mark

from teams.domain.game import Game
from teams.domain.scheduler import Scheduler
from teams.domain.team import Team


class TestScheduler(TestCase):

    def test_schedule_games(self):
        scheduler = Scheduler()
        result = scheduler.schedule_games(["team 1", "team 2", "team 3", "team 4", "team 5"], "55", 25, 1, False)
        print()
        print("Game List")
        for x in result:
            print(str(x.day) + ": " + x.home_id + " vs " + x.away_id)

        print("Total Games: " + str(len(result)))

    def test_setup_matrix_odd(self):
        scheduler = Scheduler()
        scheduler.total_teams = 5
        scheduler.setup()
        scheduler.pairs = 3
        scheduler.odd = True

        self.assertEqual(-1, scheduler.anchor)

        assert [0, 1, 2, 3, 4] == scheduler.num_list

    def test_setup_matrix_even(self):
        scheduler = Scheduler()
        scheduler.total_teams = 6
        scheduler.setup()
        scheduler.pairs = 3
        scheduler.odd = False

        self.assertEqual(0, scheduler.anchor)

        assert [1, 2, 3, 4, 5] == scheduler.num_list

    def test_incrementer_even(self):
        scheduler = Scheduler()
        scheduler.total_teams = 6
        scheduler.setup()

        scheduler.populate_matrix()
        assert [[0, 1],
               [2, 5],
               [3, 4]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[0, 2],
               [3, 1],
               [4, 5]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[0, 3],
               [4, 2],
               [5, 1]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[0, 4],
               [5, 3],
               [1, 2]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[0, 5],
               [1, 4],
               [2, 3]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[0, 1],
               [2, 5],
               [3, 4]] == scheduler.matrix

    def test_incrementer_odd(self):
        scheduler = Scheduler()
        scheduler.total_teams = 5
        scheduler.setup()

        scheduler.populate_matrix()
        assert [[-1, 0],
               [1, 4],
               [2, 3]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[-1, 1],
               [2, 0],
               [3, 4]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[-1, 2],
               [3, 1],
               [4, 0]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[-1, 3],
               [4, 2],
               [0, 1]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[-1, 4],
               [0, 3],
               [1, 2]] == scheduler.matrix

        scheduler.populate_matrix()
        assert [[-1, 0],
               [1, 4],
               [2, 3]] == scheduler.matrix

    def test_does_team_play_in_games_list(self):
        team1 = Team("Team 1", 5, False)
        team2 = Team("Team 2", 5, False)
        team3 = Team("Team 3", 5, False)
        team4 = Team("Team 4", 5, False)

        game1 = Game(1, 1, team1, team2, 0, 0, False, False, None)
        game2 = Game(1, 1, team3, team4, 0, 0, False, False, None)

        game_list_1 = [game1, game2]
        game_list_2 = [game2]

        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_1, team1))
        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_1, team2))
        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_1, team3))
        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_1, team4))

        self.assertFalse(Scheduler.does_team_play_in_games_list(game_list_2, team1))
        self.assertFalse(Scheduler.does_team_play_in_games_list(game_list_2, team2))
        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_2, team3))
        self.assertTrue(Scheduler.does_team_play_in_games_list(game_list_2, team4))

    def test_does_any_team_play_in_other_list(self):
        team1 = Team("Team 1", 5, False)
        team2 = Team("Team 2", 5, False)
        team3 = Team("Team 3", 5, False)
        team4 = Team("Team 4", 5, False)
        team5 = Team("Team 5", 5, False)
        team6 = Team("Team 6", 5, False)
        team7 = Team("Team 6", 5, False)
        team8 = Team("Team 6", 5, False)

        game1 = Game(1, 1, team1, team2, 0, 0, False, False, None)
        game2 = Game(1, 1, team3, team4, 0, 0, False, False, None)
        game3 = Game(1, 1, team5, team6, 0, 0, False, False, None)

        game4 = Game(1, 1, team1, team3, 0, 0, False, False, None)
        game5 = Game(1, 1, team2, team5, 0, 0, False, False, None)
        game6 = Game(1, 1, team4, team6, 0, 0, False, False, None)

        game7 = Game(1, 1, team7, team8, 0, 0, False, False, None)

        game_list_1 = [game1, game2, game3]
        game_list_2 = [game2, game3, game4]
        game_list_3 = [game1, game2]
        game_list_4 = [game6]

        game_list_5 = [game1, game2]
        game_list_6 = [game3, game7]

        # all teams play in all other games
        self.assertTrue(Scheduler.does_any_team_play_in_other_list(game_list_1, game_list_2))

        # only one home team plays in other day
        self.assertTrue(Scheduler.does_any_team_play_in_other_list(game_list_4, game_list_3))

        # no teams play
        self.assertFalse(Scheduler.does_any_team_play_in_other_list(game_list_5, game_list_6))

    @mark.notwritten
    def test_set_day_for_new_series_game(self):
        pass

    def test_does_team_play_in_game(self):
        team1 = Team("Team 1", 5, True)
        team2 = Team("Team 2", 5, True)
        team3 = Team("Team 3", 5, True)

        game = Game(1, 1, team2, team3, 0, 0, False, False, None)

        self.assertTrue(Scheduler.does_team_play_in_game(game, team2))
        self.assertTrue(Scheduler.does_team_play_in_game(game, team3))
        self.assertFalse(Scheduler.does_team_play_in_game(game, team1))