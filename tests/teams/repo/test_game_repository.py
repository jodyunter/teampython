from unittest import TestCase

from teams.data.repo.game_repository import GameRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.game import Game, GameRules
from teams.domain.team import Team
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestGameRepository(TestBaseRepository, TestCase):
    repo = GameRepository()

    def test_add_existing_teams(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, self.get_id()), session)
        team_repo.add(Team(name_2, 12, self.get_id()), session)
        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = team_repo.get_by_name(name_2, session)

        self.repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                           self.get_id()), session)
        session.commit()

        g_list = self.repo.get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_no_existing_teams(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_1 = Team(name_1, 12, self.get_id())
        team_2 = Team(name_2, 12, self.get_id())

        self.repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                           self.get_id()), session)
        session.commit()

        g_list = self.repo.get_all(session)
        self.assertEqual(1, len(g_list))

    def test_add_one_existing_team(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, self.get_id()), session)

        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = Team(name_2, 12, self.get_id())

        self.repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                           self.get_id()), session)
        session.commit()

        g_list = self.repo.get_all(session)
        self.assertEqual(1, len(g_list))
