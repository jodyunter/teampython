from unittest import TestCase

from teams.data.database import Database
from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_team import TeamDTO
from teams.data.repo.game_repository import GameRepository
from teams.data.repo.game_rules_repository import GameRulesRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.game import Game, GameRules
from teams.domain.team import Team
from tests.teams.repo.test_repository import BaseRepoTests


class GameRepoTests(BaseRepoTests, TestCase):

    def test_add_record(self):
        return BaseRepoTests.test_add_record(self)

    def get_add_record(self):
        return GameDTO(Game(1, 2,
                            TeamDTO(Team("Home team", 250, True)),
                            TeamDTO(Team("Away Team", 251, False)),
                            3, 4, False, True, GameRulesDTO(GameRules("Rules Name", False))))

    def get_updated_record(self, original_record):
        original_record.day = 10
        original_record.year = 20
        original_record.home_team = TeamDTO(Team("New Home TEam", 249, False))
        original_record.away_team = TeamDTO(Team("New Away TEam", 244, True))
        original_record.home_score = 30
        original_record.away_score = 30
        original_record.complete = True
        original_record.processed = False
        original_record.rules = GameRulesDTO(GameRules("Rules Name 2", False))
        return original_record

    def test_add_existing_teams(self):
        session = self.setup_basic_test()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        TeamRepository.add(Team(name_1, 12, True, self.get_id()), TeamDTO, session)
        TeamRepository.add(Team(name_2, 12, True, self.get_id()), TeamDTO, session)
        session.commit()

        team_1 = TeamRepository.get_by_name(name_1, session)
        team_2 = TeamRepository.get_by_name(name_2, session)

        GameRepository.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                                self.get_id()), GameDTO, session)
        session.commit()

        g_list = GameRepository.get_all(GameDTO, session)
        self.assertEqual(1, len(g_list))

    def test_add_no_existing_teams(self):
        session = self.setup_basic_test()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_1 = Team(name_1, 12, True, self.get_id())
        team_2 = Team(name_2, 12, True, self.get_id())

        GameRepository.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                                self.get_id()), GameDTO, session)
        session.commit()

        g_list = GameRepository.get_all(GameDTO, session)
        self.assertEqual(1, len(g_list))

    def test_add_one_existing_team(self):
        session = self.setup_basic_test()
        team_repo = TeamRepository()
        repo = GameRepository()

        name_1 = "Team GA1"
        name_2 = "Team GA2"

        team_repo.add(Team(name_1, 12, True, self.get_id()), TeamDTO, session)

        session.commit()

        team_1 = team_repo.get_by_name(name_1, session)
        team_2 = Team(name_2, 12, True, self.get_id())

        repo.add(Game(1, 15, team_1, team_2, 5, 4, True, False, GameRules("Rules", True, self.get_id()),
                      self.get_id()), GameDTO, session)
        session.commit()

        g_list = repo.get_all(GameDTO, session)
        self.assertEqual(1, len(g_list))

    def test_get_my_complete_and_unprocessed(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)

        team1 = Team("t1", 5, True, "A")
        team2 = Team("t2", 5, True, "B")
        TeamRepository.add(team1, TeamDTO, session)
        TeamRepository.add(team2, TeamDTO, session)
        gr = GameRules("Rules 12", True, "T")
        GameRulesRepository.add(gr, GameRulesDTO, session)
        session.commit()

        team1 = TeamRepository.get_by_name("t1", session)
        team2 = TeamRepository.get_by_name("t2", session)
        gr = GameRulesRepository.get_by_name("Rules 12", session)

        game1 = Game(1, 1, team1, team2, 0, 0, True, False, gr, "1")
        game2 = Game(1, 1, team1, team2, 0, 0, False, False, gr, "2")
        game3 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "3")
        game4 = Game(1, 2, team1, team2, 0, 0, False, False, gr, "4")
        game5 = Game(1, 3, team1, team2, 0, 0, True, False, gr, "5")
        game6 = Game(1, 3, team1, team2, 0, 0, False, False, gr, "6")
        game7 = Game(1, 4, team1, team2, 0, 0, True, False, gr, "7")
        game8 = Game(2, 1, team1, team2, 0, 0, True, False, gr, "8")

        games = [game1, game2, game3, game4, game5, game6, game7, game8]

        [GameRepository.add(g, GameDTO, session) for g in games]

        session.commit()

        result = list(GameRepository.get_by_unprocessed_and_complete(1, 1, 4, session))
        self.assertEqual(3, len(result))

        result = list(GameRepository.get_by_unprocessed_and_complete(1, 1, 2, session))
        self.assertEqual(1, len(result))

        result = list(GameRepository.get_by_unprocessed_and_complete(2, 1, 25, session))
        self.assertEqual(1, len(result))

    def test_get_first_day_for_game(self):
        session = self.setup_basic_test()
        Database.clean_up_database(session)

        team1 = Team("t1", 5, True, "A")
        team2 = Team("t2", 5, True, "B")
        team3 = Team("t3", 5, True, "C")
        team4 = Team("t4", 5, True, "D")

        new_teams = [team1, team2, team3, team4]
        [TeamRepository.add(team, TeamDTO, session) for team in new_teams]

        new_gr = GameRules("Rules 12", True, "T")
        GameRulesRepository.add(new_gr, GameRulesDTO, session)
        session.commit()

        gr = GameRulesRepository.get_by_name("Rules 12", session)

        teams = TeamRepository.get_all(TeamDTO, session)

        game1 = Game(1, 5, teams[0], teams[1], 0, 1, True, True, gr, "K")

        games = [game1]

        [GameRepository.add(game, GameDTO, session) for game in games]

        session.commit()
        # first test, should be none because teams[0] plays on day 5
        game2 = GameDTO(Game(1, -1, teams[0], teams[2], 0, 1, True, True, gr, "K"))
        result = GameRepository.get_first_day_for_game(1, 5, game2, session).scalar()

        pass