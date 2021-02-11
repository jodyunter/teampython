from unittest import TestCase

from teams.domain.scheduler import Scheduler


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
        raise NotImplementedError

    def test_does_any_team_play_in_other_list(self):
        raise NotImplementedError

    def test_set_day_for_new_series_game(self):
        raise NotImplementedError
