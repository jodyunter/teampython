from unittest import TestCase

import pytest
from pytest import mark

from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition import Competition, CompetitionTeam
from teams.domain.competition_configuration import SubCompetitionConfiguration, CompetitionGroupConfiguration, CompetitionTeamConfiguration
from teams.domain.errors import DomainError
from teams.domain.sub_competition import TableSubCompetition
from teams.domain.team import Team


class TestCompConfiguratorGroups(TestCase):

    def test_should_not_create_group_competition_not_there(self):
        with pytest.raises(DomainError, match="Competition has to exist before the groups can be setup."):
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1,
                                                          SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                          None)
            comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                     CompetitionGroupConfiguration.RANKING_TYPE,
                                                                     1, None)
            comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config,
                                                              comp_parent_group_config, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE,
                                                              1, None)
            current_groups = []
            group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, None)

    def test_should_not_create_group_sub_competition_does_not_exist(self):
        with pytest.raises(DomainError, match="You are setting up groups before sub competitions."):
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1,
                                                          SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                          None)
            comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                     CompetitionGroupConfiguration.RANKING_TYPE,
                                                                     1, None)
            comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config,
                                                              comp_parent_group_config, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE,
                                                              1, None)

            current_groups = []

            competition = Competition("My Comp", 1, [], False, False, False, False)

            group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)

    def test_should_create_group_no_parent(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)
        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)

        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(1, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))

    def test_should_create_group_group_already_setup(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)
        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        # try it again
        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(1, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))

    def test_should_create_group_parent_not_created(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)

        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNotNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        parent = group.parent_group
        self.assertEqual("Parent 1 Config", parent.name)
        self.assertEqual(parent.sub_competition.oid, sub_comp.oid)
        self.assertEqual(parent.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(parent.rankings))

        self.assertEqual(2, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent.oid]))

    def test_should_create_group_parent_already_created(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)

        parent = CompetitionConfigurator.create_competition_group(comp_parent_group_config, current_groups, competition)
        self.assertEqual(1, len(current_groups))
        self.assertEqual("Parent 1 Config", parent.name)
        self.assertEqual(parent.sub_competition.oid, sub_comp.oid)
        self.assertEqual(parent.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(parent.rankings))

        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)

        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNotNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(2, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent.oid]))

    def test_should_create_group_multiple_parents(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config2 = CompetitionGroupConfiguration("Parent 2 Config", sub_comp_config, None, 1,
                                                                  CompetitionGroupConfiguration.RANKING_TYPE,
                                                                  1, None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config,
                                                                 comp_parent_group_config2, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        parent = group.parent_group
        parent_parent = parent.parent_group

        self.assertEqual(3, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent_parent.oid]))

    def test_should_create_group_top_parent_exists_middle_does_not(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config2 = CompetitionGroupConfiguration("Parent 2 Config", sub_comp_config, None, 1,
                                                                  CompetitionGroupConfiguration.RANKING_TYPE,
                                                                  1, None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config,
                                                                 comp_parent_group_config2, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        current_groups = []

        competition = Competition("My Comp", 1, [], False, False, False, False)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, 1, False, False, False, False)
        competition.sub_competitions.append(sub_comp)
        parent_parent = CompetitionConfigurator.create_competition_group(comp_parent_group_config2, current_groups, competition)
        group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        parent = group.parent_group

        self.assertIsNotNone(parent.parent_group)
        self.assertEqual(parent_parent.oid, parent.parent_group.oid)
        self.assertEqual(3, len(current_groups))
        self.assertEqual(1, len([g for g in current_groups if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent.oid]))
        self.assertEqual(1, len([g for g in current_groups if g.oid == parent_parent.oid]))


class TestCompConfiguratorTeams(TestCase):

    def test_should_fail_competition_no_created(self):
        with pytest.raises(DomainError, match="Competition has to exist before the teams and rankings can be setup."):
            CompetitionConfigurator.process_competition_team_configuration(None, None, None, None)

    def test_should_fail_no_team_configuration(self):
        with pytest.raises(DomainError, match="No team configuration given."):
            competition = Competition("My Comp", 1, [], False, False, False, False)
            CompetitionConfigurator.process_competition_team_configuration(None, [], [], competition)

    def test_should_fail_group_not_created(self):
        with pytest.raises(DomainError, match="Group Team Group 1 has not been created yet."):
            competition = Competition("My Comp", 1, [], False, False, False, False)
            comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, None, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, [], [], competition)

    def test_should_fail_too_many_groups(self):
        with pytest.raises(DomainError, match="Group Team Group 1 has multiple groups 2."):
            competition = Competition("My Comp", 1, [], False, False, False, False)
            comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, None, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
            current_groups = []
            comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
            current_groups.append(comp_group)
            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, [], competition)

    def test_should_fail_too_many_teams(self):
        with pytest.raises(DomainError, match=r"Team My Team has too many 2 teams created."):
            competition = Competition("My Comp", 1, [], False, False, False, False)
            comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, None, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
            current_groups = []
            comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            comp_team = CompetitionTeam(competition, team)
            current_teams = [comp_team, comp_team]
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, current_teams, competition)

    def test_should_add_team_team_does_not_exist(self):
        competition = Competition("My Comp", 1, [], False, False, False, False)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, None, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        current_groups = []
        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        current_teams = []
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, current_teams, competition)

        self.assertEqual(1, len(current_teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(team.oid, comp_group.rankings[0].team.parent_team.oid)

    def test_should_add_team_team_exists(self):
        competition = Competition("My Comp", 1, [], False, False, False, False)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, None, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        current_groups = []
        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        current_teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, current_teams, competition)

        self.assertEqual(1, len(current_teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)

    def test_should_add_team_multiple_parents(self):
        competition = Competition("My Comp", 1, [], False, False, False, False)
        parent_comp_group_config = CompetitionGroupConfiguration("Parent Group 1", None, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, parent_comp_group_config, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        current_groups = []
        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        self.assertEqual(2, len(current_groups))
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        current_teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, current_teams, competition)

        self.assertEqual(1, len(current_teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(1, len(comp_group.parent_group.rankings))
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)
        self.assertEqual(comp_team.oid, comp_group.parent_group.rankings[0].team.oid)

    def test_should_add_multiple_teams(self):
        competition = Competition("My Comp", 1, [], False, False, False, False)
        parent_comp_group_config = CompetitionGroupConfiguration("Parent Group 1", None, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", None, parent_comp_group_config, 1, CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        current_groups = []
        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, competition)
        self.assertEqual(2, len(current_groups))
        team = Team("My Team", 5, True)
        team2 = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        competition_team_configuration2 = CompetitionTeamConfiguration(team2, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        current_teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, current_groups, current_teams, competition)
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration2, current_groups,
                                                                       current_teams, competition)

        self.assertEqual(2, len(current_teams))
        self.assertEqual(2, len(comp_group.rankings))
        self.assertEqual(2, len(comp_group.parent_group.rankings))
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)
        self.assertEqual(comp_team.oid, comp_group.parent_group.rankings[0].team.oid)
        self.assertEqual(current_teams[1].oid, comp_group.rankings[1].team.oid)
        self.assertEqual(current_teams[1].oid, comp_group.parent_group.rankings[1].team.oid)


class TestCompConfiguratorCompGame(TestCase):

    @mark.notwritten
    def test_should_process_comp_game_with_series(self):
        pass

    @mark.notwritten
    def test_should_process_comp_game_with_table(self):
        pass


class TestCompConfiguratorTableGames(TestCase):

    @mark.notwritten
    def test_should_process_table_game(self):
        # need multiple types
        pass


class TestCompConfiguratorSeriesGames(TestCase):

    @mark.notwritten
    def should_process_by_goals_method(self):
        pass

    @mark.notwritten
    def should_process_by_wins_method(self):
        pass

    @mark.notwritten
    def should_process_series_with_by_wins(self):
        pass

    @mark.notwritten
    def should_process_series_with_by_goals(self):
        pass
