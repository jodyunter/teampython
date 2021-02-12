from unittest import TestCase

from teams.domain.competition import Competition, CompetitionGroup, CompetitionRanking
from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.game import GameRules
from teams.domain.series import SeriesByGoals, SeriesGame, SeriesByWins
from teams.domain.series_rules import SeriesByGoalsRules, SeriesByWinsRules
from teams.domain.sub_competition import PlayoffSubCompetition
from tests.teams.domain.competition import helpers


class TestPlayoffSubCompetition(TestCase):
    @staticmethod
    def create_default_playoff(groups):
        competition = Competition("My Comp", 1, [], False, False, False, False)
        playoff = PlayoffSubCompetition("Playoff", [], competition, 1, 1, False, False, False, False)
        competition.sub_competitions.append(playoff)

        league = CompetitionGroup("League", None, None, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r1_winners_group = CompetitionGroup("R1 Winners", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)
        r1_losers_group = CompetitionGroup("R1 Losers", None, playoff, [], CompetitionGroupConfiguration.RANKING_TYPE)

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

        groups.extend([league, r1_winners_group, r1_losers_group])

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

        playoff.series.extend([series1, series2, series3, series4])

        return playoff

    def test_process_game(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)
        self.assertIsNotNone(groups)
        self.assertEqual(3, len(groups))
        series = playoff.series[2]

        game = SeriesGame(series, 1, series.sub_competition.competition, series.sub_competition, 5,
                          series.home_team, series.away_team, 5, 3, True, False, None)

        playoff.process_game(game)

        for s in playoff.series:
            if s.oid == series.oid:
                self.assertEqual(1, s.games_played)
            else:
                self.assertEqual(0, s.games_played)

    #  for the purposes of this test, it requires setup round to work properly
    def test_create_games(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)
        new_games = playoff.create_new_games([])

        for s in playoff.series:
            games = [g for g in new_games if g.series.oid == s.oid]
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

    def test_is_complete(self):
        raise NotImplementedError

    def test_create_status_map(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)
        new_games = playoff.create_new_games([])

        series1_games = [g for g in new_games if g.series.name == "Series 1"]
        series2_games = [g for g in new_games if g.series.name == "Series 2"]
        series3_games = [g for g in new_games if g.series.name == "Series 3"]
        series4_games = [g for g in new_games if g.series.name == "Series 4"]

        series3_games[0].complete = True
        series3_games[0].processed = True

        series1_games[1].complete = True
        series1_games[1].processed = True

        series4_games[3].complete = True
        series4_games[3].processed = True

        status_map = playoff.create_series_map(new_games)

        for s in playoff.series:
            games = [g for g in new_games if g.series.oid == s.oid]
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
                self.assertFalse(True, "Why are we here?")

    def test_setup_round_1(self):
        groups = []
        playoff = TestPlayoffSubCompetition.create_default_playoff(groups)

        playoff.setup_round(1)

        for s in playoff.series:
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
                self.assertFalse(True, "Why are we here?")

    def test_setup_round_2(self):
        raise NotImplementedError

    def test_post_process_round(self):
        raise NotImplementedError

    def test_is_round_complete(self):
        # test normal case

        # test we have no series cases
        raise NotImplementedError

    def test_is_round_post_processed(self):
        raise NotImplementedError

    def test_is_round_setup(self):
        raise NotImplementedError

