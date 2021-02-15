from unittest import TestCase

from pytest import mark

from teams.domain.competition import CompetitionGroup
from teams.domain.competition_configuration import CompetitionGroupConfiguration
from tests.teams.domain.competition import helpers


class TestCompetitionGroup(TestCase):

    @mark.notwritten
    def test_add_team_to_group_again(self):
        pass

    @mark.notwritten
    def test_add_team_to_group_no_rank(self):
        pass

    def test_add_team_to_group(self):
        group = CompetitionGroup("My Group", None, None, None, CompetitionGroupConfiguration.RANKING_TYPE)
        rankings = []
        group.rankings = rankings

        group.add_team_to_group(helpers.new_comp_team(None, "Team 1", 5), 5)
        self.assertEqual(1, len(group.rankings))
        self.assertEqual(5, group.rankings[0].rank)

        group.add_team_to_group(helpers.new_comp_team(None, "Team 2", 5), 25)
        self.assertEqual(2, len(group.rankings))
        self.assertEqual(25, group.rankings[1].rank)

    def test_should_get_team_by_order(self):
        group = CompetitionGroup("My Group", None, None, None, CompetitionGroupConfiguration.RANKING_TYPE)
        rankings = []
        group.rankings = rankings

        group.add_team_to_group(helpers.new_comp_team(None, "Team 1", 5), 5)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 2", 5), 45)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 3", 5), 65)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 4", 5), 35)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 5", 5), 25)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 6", 5), 15)

        self.assertEqual(6, len(group.rankings))

        self.assertEqual("Team 1", group.get_team_by_order(1).team.name)
        self.assertEqual("Team 2", group.get_team_by_order(5).team.name)
        self.assertEqual("Team 3", group.get_team_by_order(6).team.name)
        self.assertEqual("Team 4", group.get_team_by_order(4).team.name)
        self.assertEqual("Team 5", group.get_team_by_order(3).team.name)
        self.assertEqual("Team 6", group.get_team_by_order(2).team.name)

    # TODO: we don't really handle errors or missing ranks yet
    def test_should_get_team_by_rank(self):
        group = CompetitionGroup("My Group", None, None, None, CompetitionGroupConfiguration.RANKING_TYPE)
        rankings = []
        group.rankings = rankings

        group.add_team_to_group(helpers.new_comp_team(None, "Team 1", 5), 5)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 2", 5), 45)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 3", 5), 65)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 4", 5), 35)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 5", 5), 25)
        group.add_team_to_group(helpers.new_comp_team(None, "Team 6", 5), 15)

        self.assertEqual(6, len(group.rankings))

        self.assertEqual("Team 1", group.get_team_by_rank(5).team.name)
        self.assertEqual("Team 2", group.get_team_by_rank(45).team.name)
        self.assertEqual("Team 3", group.get_team_by_rank(65).team.name)
        self.assertEqual("Team 4", group.get_team_by_rank(35).team.name)
        self.assertEqual("Team 5", group.get_team_by_rank(25).team.name)
        self.assertEqual("Team 6", group.get_team_by_rank(15).team.name)

    @mark.notwritten
    def test_get_rank_for_team(self):
        pass


class TestCompetitionRanking(TestCase):

    @mark.notwritten
    def test_get_dictionary_of_groups_from_rankings(self):
        pass
