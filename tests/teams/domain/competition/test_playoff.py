import numpy as np
from pytest import mark

from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.competition_group import CompetitionGroup
from teams.domain.competition_ranking import CompetitionRanking
from teams.domain.game_rules import GameRules
from teams.domain.series_by_goals import SeriesByGoals
from teams.domain.series_by_goals_rules import SeriesByGoalsRules
from teams.domain.series_by_wins import SeriesByWins
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.domain.series_game import SeriesGame
from teams.domain.sub_competition import PlayoffSubCompetition
from tests.teams.domain.competition import helpers
from tests.teams.domain.competition.helpers import create_default_competition_for_testing
from tests.teams.domain.competition.test_configurator import BaseTeamTestCase


class TestPlayoffSubCompetition(BaseTeamTestCase):
    SEED = 1234

    @staticmethod
    def play_current_round(playoff, games, process_round=False):
        while not playoff.is_round_complete(playoff.current_round):
            new_games = playoff.create_new_games(current_games=[])
            games.extend(new_games)

            for g in new_games:
                g.play()
                playoff.process_game(g)

        if process_round:
            playoff.post_process_round(playoff.current_round)

    @staticmethod
    def create_default_playoff(groups):
        competition = create_default_competition_for_testing("My Comp")
        playoff = PlayoffSubCompetition("Playoff", [], competition, None, 1, 1, False, False, False, False)
        competition.sub_competitions.append(playoff)

        league = CompetitionGroup("League", None, None, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r1_winners_group = CompetitionGroup("R1 Winners", None, playoff, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r1_losers_group = CompetitionGroup("R1 Losers", None, playoff, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r2_winners_group = CompetitionGroup("R2 Winners", None, playoff, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r2_losers_group = CompetitionGroup("R2 Losers", None, playoff, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        eliminated = CompetitionGroup("Eliminated Group", None, playoff, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)

        league.rankings = [
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 1", 5), 1),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 2", 5), 2),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 3", 5), 3),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 4", 5), 4),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 5", 5), 5),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 6", 5), 6),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 7", 5), 7),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 8", 5), 8),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 9", 5), 9),
            CompetitionRanking(league, helpers.new_comp_team(competition, "Team 10", 5), 10),
        ]

        groups.extend([league, r1_winners_group, r1_losers_group, r2_winners_group, r2_losers_group, eliminated])

        game_rules_tie = GameRules("Can Tie", True)
        game_rules_no_tie = GameRules("No Tie", False)

        series_rules_by_goals_2 = SeriesByGoalsRules("By Goals 2 Games", 2, game_rules_tie, game_rules_no_tie, None)
        series_rules_by_goals_3 = SeriesByGoalsRules("By Goals 3 Games", 3, game_rules_tie, game_rules_no_tie, None)
        series_rules_by_goals_1 = SeriesByGoalsRules("By Goals 1 Games", 1, game_rules_tie, game_rules_no_tie, None)
        series_rules_wins_4 = SeriesByWinsRules("4 wins", 4, game_rules_no_tie, [0, 0, 1, 1, 0, 1, 0])

        series1 = SeriesByGoals(playoff, "Series 1", 1, None, None, 0, 0, 0, series_rules_by_goals_2,
                                league, 1, league, 8, r1_winners_group, league, r1_losers_group, league, False, False)

        series2 = SeriesByGoals(playoff, "Series 2", 1, None, None, 0, 0, 0, series_rules_by_goals_3,
                                league, 2, league, 7, r1_winners_group, league, r1_losers_group, league, False, False)

        series3 = SeriesByGoals(playoff, "Series 3", 1, None, None, 0, 0, 0, series_rules_by_goals_1,
                                league, 3, league, 6, r1_winners_group, league, r1_losers_group, league, False, False)

        series4 = SeriesByWins(playoff, "Series 4", 1, None, None, 0, 0, series_rules_wins_4,
                               league, 4, league, 5, r1_winners_group, league, r1_losers_group, league, False, False)

        series5 = SeriesByWins(playoff, "Series 5", 2, None, None, 0, 0, series_rules_wins_4,
                               r1_winners_group, 1, r1_winners_group, 4, r2_winners_group, league, r2_losers_group, league, False, False)

        series6 = SeriesByGoals(playoff, "Series 6", 2, None, None, 0, 0, 0, series_rules_by_goals_1,
                                r1_winners_group, 2, r1_winners_group, 3, r2_winners_group, league, r2_losers_group, league, False, False)

        series7 = SeriesByGoals(playoff, "Series 7", 2, None, None, 0, 0, 0, series_rules_by_goals_1,
                                r1_losers_group, 1, league, 2, r1_losers_group, eliminated, league, eliminated, league, False, False)

        playoff.series_configurations.extend([series1, series2, series3, series4, series5, series6, series7])

        return playoff

    def test_process_game(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)
        self.assertIsNotNone(groups)
        self.assertEqual(6, len(groups))
        series = playoff.series_configurations[2]

        game = SeriesGame(series, 1, series.sub_competition.competition, series.sub_competition, 5,
                          series.home_team, series.away_team, 5, 3, True, False, None)

        playoff.process_game(game)

        for s in [s for s in playoff.series_configurations if s.series_round == 1]:
            if s.oid == series.oid:
                self.assertEqual(1, s.games_played)
            else:
                if isinstance(s, SeriesByWins):
                    self.assertEqual(s.home_wins, s.away_wins)
                    self.assertEqual(0, s.home_wins)
                else:
                    self.assertEqual(0, s.games_played)

    #  for the purposes of this test, it requires setup round to work properly
    def test_create_games(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)
        new_games = playoff.create_new_games(current_games=[])

        for s in [s for s in playoff.series_configurations if s.series_round == 1]:
            games = [g for g in new_games if g.series_configurations.oid == s.oid]
            number_of_games = len(games)
            if s.name == "Series 1":
                self.assertEqual(2, number_of_games)
            elif s.name == "Series 2":
                self.assertEqual(3, number_of_games)
            elif s.name == "Series 3":
                self.assertEqual(1, number_of_games)
            elif s.name == "Series 4":
                self.assertEqual(4, number_of_games)
            else:
                self.assertFalse(True, "Why are we here?")

    @mark.notwritten
    def test_is_complete(self):
        pass

    def test_create_status_map(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)
        new_games = playoff.create_new_games(current_games=[])

        series1_games = [g for g in new_games if g.series_configurations.name == "Series 1"]
        series2_games = [g for g in new_games if g.series_configurations.name == "Series 2"]
        series3_games = [g for g in new_games if g.series_configurations.name == "Series 3"]
        series4_games = [g for g in new_games if g.series_configurations.name == "Series 4"]

        series3_games[0].complete = True
        series3_games[0].processed = True

        series1_games[1].complete = True
        series1_games[1].processed = True

        series4_games[3].complete = True
        series4_games[3].processed = True

        status_map = playoff.create_series_map(new_games)

        for s in playoff.series_configurations:
            games = [g for g in new_games if g.series_configurations.oid == s.oid]
            number_of_games = len(games)
            if s.name == "Series 1":
                self.assertEqual(1, status_map["Complete Games"][s.oid], "S1C")
                self.assertEqual(1, status_map["Incomplete Games"][s.oid], "S1I")
            elif s.name == "Series 2":
                self.assertEqual(0, status_map["Complete Games"][s.oid], "S2C")
                self.assertEqual(3, status_map["Incomplete Games"][s.oid], "S2C")
            elif s.name == "Series 3":
                self.assertEqual(1, status_map["Complete Games"][s.oid], "S3C")
                self.assertEqual(0, status_map["Incomplete Games"][s.oid], "S3C")
            elif s.name == "Series 4":
                self.assertEqual(1, status_map["Complete Games"][s.oid], "S4C")
                self.assertEqual(3, status_map["Incomplete Games"][s.oid], "S4C")
            else:
                self.assertEqual(0, status_map["Complete Games"][s.oid], "Other")
                self.assertEqual(0, status_map["Incomplete Games"][s.oid], "Other")

    def test_setup_round_1(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)

        for s in playoff.series_configurations:
            if s.name == "Series 1":
                self.assertEqual("Team 1", s.home_team.name, "S1H")
                self.assertEqual("Team 8", s.away_team.name, "S1A")
            elif s.name == "Series 2":
                self.assertEqual("Team 2", s.home_team.name, "S2H")
                self.assertEqual("Team 7", s.away_team.name, "S2A")
            elif s.name == "Series 3":
                self.assertEqual("Team 3", s.home_team.name, "S3H")
                self.assertEqual("Team 6", s.away_team.name, "S3A")
            elif s.name == "Series 4":
                self.assertEqual("Team 4", s.home_team.name, "S4H")
                self.assertEqual("Team 5", s.away_team.name, "S4A")
            else:
                self.assertIsNone(s.home_team)
                self.assertIsNone(s.away_team)

    def test_setup_round_2(self):
        # was round 1 complete?
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)
        playoff.setup = True
        playoff.setup_round(1)

        self.assertFalse(playoff.is_round_complete(1))

        np.random.seed =  TestPlayoffSubCompetition.SEED

        games = []
        TestPlayoffSubCompetition.play_current_round(playoff, games)
        self.assertTrue(playoff.is_round_complete(1))
        self.assertFalse(playoff.is_round_post_processed(1))
        playoff.post_process_round(1)
        self.assertTrue(playoff.is_round_post_processed(1))
        playoff.current_round += 1
        playoff.setup_round(playoff.current_round)
        series = playoff.get_series_for_round(2)
        self.assertEqual(3, len(series))
        for s in series:
            self.assertTrue(s.setup)
            self.assertFalse(s.is_complete())
        # was round 1 post processed

    def test_post_process_round(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)
        playoff.setup_round(1)
        playoff.setup = True

        self.assertEqual(10, len(groups[0].rankings))
        self.assertEqual(0, len(groups[1].rankings))
        self.assertEqual(0, len(groups[2].rankings))

        np.random.seed = TestPlayoffSubCompetition.SEED

        games = []
        TestPlayoffSubCompetition.play_current_round(playoff, games)

        playoff.post_process_round(playoff.current_round)

        for s in [a for a in playoff.series_configurations if a.series_round == 1]:
            self.assertTrue(s.is_complete())
            self.assertTrue(s.post_processed)

        # winners are team 1, 7, 3, 4
        # losers are team 8, 2, 6, 5
        self.assertEqual(4, len(groups[1].rankings))
        self.assertEqual(4, len(groups[2].rankings))
        self.assertEqual(0, len(groups[3].rankings))
        self.assertEqual(0, len(groups[4].rankings))

    @mark.notwritten
    def test_is_round_complete(self):
        # test normal case
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)
        # test we have no series cases
        pass

