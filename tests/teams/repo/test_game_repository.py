from unittest import TestCase

from teams.data.database import Database
from teams.data.repo.game_repository import GameRepository
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.game import Game, GameRules
from teams.domain.team import Team
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestGameRepository(TestBaseRepository, TestCase):
    def test_add_existing_teams(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        repo = GameRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, True, self.get_id()), session)
        team_repo.add(Team(name_2, 12, True, self.get_id()), session)
        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = team_repo.get_by_name(name_2, session)

        repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                      self.get_id()), session)
        session.commit()

        g_list = repo.get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_no_existing_teams(self):
        session = self.setup_basic_test()
        repo = GameRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_1 = Team(name_1, 12, True, self.get_id())
        team_2 = Team(name_2, 12, True, self.get_id())

        repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                      self.get_id()), session)
        session.commit()

        g_list = repo.get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_one_existing_team(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        repo = GameRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, True, self.get_id()), session)

        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = Team(name_2, 12, True, self.get_id())

        repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                      self.get_id()), session)
        session.commit()

        g_list = repo.get_all(session)
        self.assertEqual(1, len(g_list))

    def test_get_my_complete_and_unprocessed(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)
        repo = GameRepository()
        team_repo = TeamRepository()
        gr_repo = GameRulesRepository()

        team1 = Team("t1", 5, True, "A")
        team2 = Team("t2", 5, True, "B")
        team_repo.add(team1, session)
        team_repo.add(team2, session)
        gr = GameRules("Rules 12", True, "T")
        gr_repo.add(gr, session)
        session.commit()

        team1 = team_repo.get_by_name("t1", session)
        team2 = team_repo.get_by_name("t2", session)
        gr = gr_repo.get_by_name("Rules 12", session)

        game1 = Game(1, 1, team1, team2, 0, 0, True, False, gr, "1")
        game2 = Game(1, 1, team1, team2, 0, 0, False, False, gr, "2")
        game3 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "3")
        game4 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "4")
        game5 = Game(1, 3, team1, team2, 0, 0, True, False, gr, "5")
        game6 = Game(1, 3, team1, team2, 0, 0, False, False, gr, "6")
        game7 = Game(1, 4, team1, team2, 0, 0, True, False, gr, "7")
        game8 = Game(2, 1, team1, team2, 0, 0, True, False, gr, "8")

        games = [game1, game2, game3, game4, game5, game6, game7, game8]

        [repo.add(g, session) for g in games]

        session.commit()

        result = list(repo.get_by_unprocessed_and_complete(1, 1, 4, session))
        self.assertEqual(3, len(result))

        result = list(repo.get_by_unprocessed_and_complete(1, 1, 2, session))
        self.assertEqual(1, len(result))

        result = list(repo.get_by_unprocessed_and_complete(2, 1, 25, session))
        self.assertEqual(1, len(result))
