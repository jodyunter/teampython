from unittest import TestCase

from teams.data.database import Database
from teams.data.repo.game_repository import GameRepository, CompetitionGameRepository, SeriesGameRepository
from teams.data.repo.rules_repository import GameRulesRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.competition import Competition
from teams.domain.competition_game import CompetitionGame
from teams.domain.competition_team import CompetitionTeam
from teams.domain.game import Game
from teams.domain.game_rules import  GameRules
from teams.domain.table_sub_competition import TableSubCompetition
from teams.domain.team import Team
from tests.teams.repo.test_repository import BaseRepoTests


class GameRepoTests(BaseRepoTests, TestCase):

    def get_repo(self):
        return GameRepository()

    def test_add_record(self):
        return BaseRepoTests.test_add_record(self)

    def test_update_record(self):
        return BaseRepoTests.test_update_record(self)

    def get_add_record(self):
        return Game(1, 2,
                    Team("Home team", 250, True),
                    Team("Away Team", 251, False),
                    3, 4, False, True, GameRules("Rules Name", False))

    def get_updated_record(self, original_record):
        original_record.day = 10
        original_record.year = 20
        original_record.home_team = Team("New Home TEam", 249, False)
        original_record.away_team = Team("New Away TEam", 244, True)
        original_record.home_score = 30
        original_record.away_score = 30
        original_record.complete = True
        original_record.processed = False
        original_record.rules = GameRules("Rules Name 2", False)
        return original_record

    def test_add_existing_teams(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, True, self.get_id()), session)
        team_repo.add(Team(name_2, 12, True, self.get_id()), session)
        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = team_repo.get_by_name(name_2, session)

        self.get_repo().add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                                 self.get_id()), session)
        session.commit()

        g_list = self.get_repo().get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_no_existing_teams(self):
        session = self.setup_basic_test()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_1 = Team(name_1, 12, True, self.get_id())
        team_2 = Team(name_2, 12, True, self.get_id())

        self.get_repo().add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                                 self.get_id()), session)
        session.commit()

        g_list = self.get_repo().get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_one_existing_team(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, True, self.get_id()), session)

        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = Team(name_2, 12, True, self.get_id())

        self.get_repo().add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                                 self.get_id()), session)
        session.commit()

        g_list = self.get_repo().get_all(session)
        self.assertEqual(1, len(g_list))

    def create_game(self, **kwargs):
        pass

    def test_get_my_complete_and_unprocessed(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)
        team_repo = TeamRepository()
        rules_repo = GameRulesRepository()

        team1 = Team("t1", 5, True, "A")
        team2 = Team("t2", 5, True, "B")
        team_repo.add(team1, session)
        team_repo.add(team2, session)
        gr = GameRules("Rules 12", True, "T")
        rules_repo.add(gr, session)
        session.commit()

        team1 = team_repo.get_by_name("t1", session)
        team2 = team_repo.get_by_name("t2", session)
        gr = rules_repo.get_by_name("Rules 12", session)

        game1 = Game(1, 1, team1, team2, 0, 0, True, False, gr, "1")
        game2 = Game(1, 1, team1, team2, 0, 0, False, False, gr, "2")
        game3 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "3")
        game4 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "4")
        game5 = Game(1, 3, team1, team2, 0, 0, True, False, gr, "5")
        game6 = Game(1, 3, team1, team2, 0, 0, False, False, gr, "6")
        game7 = Game(1, 4, team1, team2, 0, 0, True, False, gr, "7")
        game8 = Game(2, 1, team1, team2, 0, 0, True, False, gr, "8")

        games = [game1, game2, game3, game4, game5, game6, game7, game8]

        [self.get_repo().add(g, session) for g in games]

        session.commit()

        result = list(self.get_repo().get_by_unprocessed_and_complete(1, 1, 4, session))
        self.assertEqual(3, len(result))

        result = list(self.get_repo().get_by_unprocessed_and_complete(1, 1, 2, session))
        self.assertEqual(1, len(result))

        result = list(self.get_repo().get_by_unprocessed_and_complete(2, 1, 25, session))
        self.assertEqual(1, len(result))

    # todo: still incomplete, how should we parameterized this?
    def test_get_first_day_for_game(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)
        team_repo = TeamRepository()
        rules_repo = GameRulesRepository()

        team1 = Team("t1", 5, True, "A")
        team2 = Team("t2", 5, True, "B")
        team3 = Team("t3", 5, True, "C")
        team4 = Team("t4", 5, True, "D")

        new_teams = [team1, team2, team3, team4]
        [team_repo.add(team, session) for team in new_teams]

        new_gr = GameRules("Rules 12", True, "T")
        rules_repo.add(new_gr, session)
        session.commit()

        gr = rules_repo.get_by_name("Rules 12", session)

        teams = team_repo.get_all(session)

        game1 = Game(1, 5, teams[0], teams[1], 0, 1, True, True, gr, "K")

        games = [game1]

        [self.get_repo().add(game, session) for game in games]

        session.commit()
        # first test, should be none because teams[0] plays on day 5
        game2 = Game(1, -1, teams[0], teams[2], 0, 1, True, True, gr, "L")
        result = self.get_repo().get_invalid_schedule_days(1, 1, 100, [game2.home_team.oid, game2.away_team.oid], session)

        self.assertEquals(5, result[0])

        game2.day = 1
        self.get_repo().add(game2, session)
        session.commit()

        result = self.get_repo().get_invalid_schedule_days(1, 1, 100, [game2.home_team.oid, game2.away_team.oid], session)
        self.assertTrue(5 in result)
        self.assertTrue(1 in result)

        result = self.get_repo().get_invalid_schedule_days(1, 5, 100, [game2.home_team.oid, game2.away_team.oid], session)
        self.assertTrue(5 in result)

        result = self.get_repo().get_invalid_schedule_days(1, 1, 4, [game2.home_team.oid, game2.away_team.oid], session)
        self.assertTrue(1 in result)

        result = self.get_repo().get_invalid_schedule_days(1, 2, 4, [game2.home_team.oid, game2.away_team.oid], session)
        self.assertEquals(0, len(result))

        result = self.get_repo().get_invalid_schedule_days(1, 6, 100, [game2.home_team.oid, game2.away_team.oid], session)
        self.assertEquals(0, len(result))


# todo: should probably generify the above methods to test
class CompetitionGameRepoTests(BaseRepoTests, TestCase):
    def get_repo(self):
        return CompetitionGameRepository()

    def test_add_record(self):
        return BaseRepoTests.test_add_record(self)

    # todo: should test this with a non-none competition
    def get_add_record(self):
        return CompetitionGame(Competition("test", 1, None, None, 1, False, False, False, False),
                               None, 5,
                               CompetitionTeam(None, Team("Team 1", 5, True)),
                               CompetitionTeam(None, Team("Team 2", 5, True)),
                               5, 4, True, False, None)

    def get_updated_record(self, original_record):
        original_record.day = 10
        original_record.year = 20
        original_record.home_team = Team("New Home TEam", 249, False)
        original_record.away_team = Team("New Away TEam", 244, True)
        original_record.home_score = 30
        original_record.away_score = 30
        original_record.complete = True
        original_record.processed = False
        original_record.rules = GameRules("Rules Name 2", False)
        original_record.competition = Competition("Test 2", 5, None, None, 1, False, True, True, False)
        original_record.sub_competition = TableSubCompetition("Sub Comp", None, original_record.competition, None, 1,
                                                              True, True, False, False)
        return original_record


# todo: should probably generify the above methods to test
class SeriesGameRepoTests(BaseRepoTests, TestCase):
    def get_repo(self):
        return SeriesGameRepository()

    def test_add_record(self):
        return BaseRepoTests.test_add_record(self)

    # todo: should test this with a non-none competition
    def get_add_record(self):
        return CompetitionGame(Competition("test", 1, None, None, 1, False, False, False, False),
                               None, 5,
                               CompetitionTeam(None, Team("Team 1", 5, True)),
                               CompetitionTeam(None, Team("Team 2", 5, True)),
                               5, 4, True, False, None)

    def get_updated_record(self, original_record):
        original_record.day = 10
        original_record.year = 20
        original_record.home_team = Team("New Home TEam", 249, False)
        original_record.away_team = Team("New Away TEam", 244, True)
        original_record.home_score = 30
        original_record.away_score = 30
        original_record.complete = True
        original_record.processed = False
        original_record.rules = GameRules("Rules Name 2", False)
        original_record.competition = Competition("Test 2", 5, None, None, 1, False, True, True, False)
        original_record.sub_competition = TableSubCompetition("Sub Comp", None, original_record.competition, None, 1,
                                                              True, True, False, False)
        return original_record
