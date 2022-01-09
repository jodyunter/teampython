from unittest import TestCase

import pytest
from pytest import mark

from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_configuration import SubCompetitionConfiguration, CompetitionGroupConfiguration, \
    CompetitionTeamConfiguration, SeriesConfiguration, CompetitionConfiguration, PlayoffSubCompetitionConfiguration, \
    TableSubCompetitionConfiguration
from teams.domain.competition_group import CompetitionGroup
from teams.domain.competition_team import CompetitionTeam
from teams.domain.errors import DomainError
from teams.domain.series_by_goals_rules import SeriesByGoalsRules
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.domain.sub_competition import TableSubCompetition, PlayoffSubCompetition
from teams.domain.team import Team
from tests.teams.domain.competition.helpers import create_default_competition_for_testing


class BaseTeamTestCase(TestCase):
    pass


class TestCompConfigurator(BaseTeamTestCase):

    def test_should_get_group_too_many(self):
        with pytest.raises(DomainError, match="My Group has multiple 2 entries."):
            sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
            CompetitionConfigurator.get_group_from_list(
                CompetitionGroupConfiguration("My Group", sub_comp_config, None, None, None, None, None),
                [
                    CompetitionGroup("My Group 2", None, None, None, None, None),
                    CompetitionGroup("My Group", None, None, None, None, None),
                    CompetitionGroup("My Group", None, None, None, None, None),
                    CompetitionGroup("My Group 2", None, None, None, None, None)
                ])

    def test_should_get_group_no_group(self):
        with pytest.raises(DomainError,
                           match="Group My group was not found.  Need to create group before calling this."):
            sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
            CompetitionConfigurator.get_group_from_list(
                CompetitionGroupConfiguration("My group", sub_comp_config, None, None, None, None, None),
                [
                    CompetitionGroup("My Group 2", None, None, None, None, None),
                    CompetitionGroup("My Group", None, None, None, None, None),
                    CompetitionGroup("My Group", None, None, None, None, None),
                    CompetitionGroup("My Group 2", None, None, None, None, None)])

    def test_should_get_group(self):
        sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
        result = CompetitionConfigurator.get_group_from_list(
            CompetitionGroupConfiguration("My group 3", sub_comp_config, None, None, None, None, None),
            [
                CompetitionGroup("My Group 2", None, None, None, None, None),
                CompetitionGroup("My Group", None, None, None, None, None),
                CompetitionGroup("My group 3", None, None, None, None, None),
                CompetitionGroup("My Group 2", None, None, None,
                                 None, None)])
        self.assertEqual("My group 3", result.name)


class TestCompConfigurationCompetition(BaseTeamTestCase):

    def test_should_create_competition_no_sub_comps(self):
        competition_config = CompetitionConfiguration("Comp Name", [], [], 5, 5, None)
        competition = CompetitionConfigurator.setup_competition(competition_config, 5)

        self.assertEqual("Comp Name", competition.name)
        self.assertEqual(5, competition.year)
        self.assertTrue(competition.setup)
        self.assertFalse(competition.started)
        self.assertEqual(0, len(competition.sub_competitions))
        self.assertFalse(competition.finished)
        self.assertFalse(competition.post_processed)

    @mark.notwritten
    def test_should_create_competition_full_test(self):
        # create competition, sub comps (table and playoff not in order), groups, teams etc
        pass


class TestCompConfiguratorSubCompetition(BaseTeamTestCase):

    def test_create_sub_comp_no_comp(self):
        with pytest.raises(DomainError, match="Can't setup sub competition if competition is not setup."):
            CompetitionConfigurator.create_sub_competition(
                SubCompetitionConfiguration("My Sub Comp", None, None, None, 1, None, 1, None), None)

    def test_create_sub_com_sub_comp_already_created(self):
        with pytest.raises(DomainError, match="Sub competition My Sub Comp is already setup."):
            sub_competition_configuration = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1, None, 1, None)
            sub_comp = TableSubCompetition("My Sub Comp", [], None, [], 1, False, False, False, False)
            competition = create_default_competition_for_testing("My Comp", 5, [sub_comp])

            CompetitionConfigurator.create_sub_competition(sub_competition_configuration, competition)

    def test_create_playoff_sub_comp(self):
        sub_competition_config = PlayoffSubCompetitionConfiguration("Playoff Comp", None, [], [], [], 3, 1, None)

        competition = create_default_competition_for_testing("My Comp", 5)

        sub_comp = CompetitionConfigurator.create_sub_competition(sub_competition_config, competition)

        self.assertEqual(sub_competition_config.name, sub_comp.name)
        self.assertEqual(0, len(sub_comp.series_configurations))
        self.assertEqual(competition.oid, sub_comp.competition.oid)
        self.assertEqual(sub_competition_config.order, sub_comp.order)
        self.assertFalse(sub_comp.setup)
        self.assertFalse(sub_comp.started)
        self.assertFalse(sub_comp.finished)
        self.assertFalse(sub_comp.post_processed)
        self.assertEqual(1, sub_comp.current_round, "Round")
        self.assertEqual(1, len(competition.sub_competitions), "Sub Comps")
        self.assertEqual(sub_competition_config.name, competition.sub_competitions[0].name)
        self.assertIsNotNone(sub_comp.competition)

    def test_create_table_sub_comp(self):
        sub_competition_config = SubCompetitionConfiguration("Table Sub", None, [], [], 3,
                                                             SubCompetitionConfiguration.TABLE_TYPE, 1, None)

        competition = create_default_competition_for_testing("My Comp", 5)

        sub_comp = CompetitionConfigurator.create_sub_competition(sub_competition_config, competition)

        self.assertEqual(sub_competition_config.name, sub_comp.name)
        self.assertEqual(0, len(sub_comp.records))
        self.assertEqual(competition.oid, sub_comp.competition.oid)
        self.assertEqual(sub_competition_config.order, sub_comp.order)
        self.assertFalse(sub_comp.setup)
        self.assertFalse(sub_comp.started)
        self.assertFalse(sub_comp.finished)
        self.assertFalse(sub_comp.post_processed)
        self.assertEqual(1, len(competition.sub_competitions), "Sub Comps")
        self.assertEqual(sub_competition_config.name, competition.sub_competitions[0].name)


class TestCompConfiguratorPlayoffSubComp(BaseTeamTestCase):

    def test_create_playoff_sub_comp(self):
        sub_competition_config = PlayoffSubCompetitionConfiguration("Playoff Sub Sub", None, [], [], [], 3, 1, None)

        competition = create_default_competition_for_testing("My Comp", 5)

        sub_comp = CompetitionConfigurator.create_playoff_sub_competition(sub_competition_config, competition)

        self.assertEqual(sub_competition_config.name, sub_comp.name)
        self.assertEqual(0, len(sub_comp.series_configurations))
        self.assertEqual(competition.oid, sub_comp.competition.oid)
        self.assertEqual(sub_competition_config.order, sub_comp.order)
        self.assertFalse(sub_comp.setup)
        self.assertFalse(sub_comp.started)
        self.assertFalse(sub_comp.finished)
        self.assertFalse(sub_comp.post_processed)
        self.assertEqual(1, sub_comp.current_round)


class TestCompConfiguratorTableSubComp(BaseTeamTestCase):

    def test_create_table_sub_com(self):
        sub_competition_config = TableSubCompetitionConfiguration("Table Sub", None, [], [], 3, 1, None)

        competition = create_default_competition_for_testing("My Comp", 5)

        sub_comp = CompetitionConfigurator.create_table_sub_competition(sub_competition_config, competition)

        self.assertEqual(sub_competition_config.name, sub_comp.name)
        self.assertEqual(0, len(sub_comp.records))
        self.assertEqual(competition.oid, sub_comp.competition.oid)
        self.assertEqual(sub_competition_config.order, sub_comp.order)
        self.assertFalse(sub_comp.setup)
        self.assertFalse(sub_comp.started)
        self.assertFalse(sub_comp.finished)
        self.assertFalse(sub_comp.post_processed)


class TestCompConfiguratorGroups(BaseTeamTestCase):

    def test_should_not_create_group_competition_not_there(self):
        with pytest.raises(DomainError, match="Competition has to exist before the groups can be setup."):
            competition = create_default_competition_for_testing("My Comp")
            competition.sub_competitions = [
                TableSubCompetition("My Sub Comp", None, competition, [], None, None, None, None, None)]
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, [], None, 1,
                                                          SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                          None)
            comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                     CompetitionGroupConfiguration.RANKING_TYPE,
                                                                     1, None)
            comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config,
                                                              comp_parent_group_config, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE,
                                                              1, None)

            group = CompetitionConfigurator.create_competition_group(comp_group_config, None)

    def test_should_not_create_group_sub_competition_does_not_exist(self):
        with pytest.raises(DomainError, match="You are setting up groups before sub competitions."):
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, [], None, 1,
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

            competition = create_default_competition_for_testing("My Comp")

            group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)

    def test_should_create_group_no_parent(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)

        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(1, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))

    def test_should_create_group_group_already_setup(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)
        # current_groups = []

        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        # try it again
        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(1, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))

    def test_should_create_group_parent_not_created(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)

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

        self.assertEqual(2, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent.oid]))

    def test_should_create_group_parent_already_created(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config,
                                                          1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE,
                                                          1, None)

        competition = create_default_competition_for_testing("My Comp", 3)
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        parent = CompetitionConfigurator.create_competition_group(comp_parent_group_config, competition)
        self.assertEqual(1, len(competition.get_all_groups()))
        self.assertEqual("Parent 1 Config", parent.name)
        self.assertEqual(parent.sub_competition.oid, sub_comp.oid)
        self.assertEqual(parent.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(parent.rankings))

        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)

        self.assertEqual("Group 1 Config", group.name)
        self.assertIsNotNone(group.parent_group)
        self.assertEqual(group.sub_competition.oid, sub_comp.oid)
        self.assertEqual(group.group_type, CompetitionGroupConfiguration.RANKING_TYPE)
        self.assertEqual(0, len(group.rankings))

        self.assertEqual(2, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent.oid]))

    def test_should_create_group_multiple_parents(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
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

        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        parent = group.parent_group
        parent_parent = parent.parent_group

        self.assertEqual(3, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent_parent.oid]))

    def test_should_create_group_top_parent_exists_middle_does_not(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, None, None, 1,
                                                      SubCompetitionConfiguration.TABLE_TYPE, 1,
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

        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        parent_parent = CompetitionConfigurator.create_competition_group(comp_parent_group_config2, competition)
        group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        parent = group.parent_group

        self.assertIsNotNone(parent.parent_group)
        self.assertEqual(parent_parent.oid, parent.parent_group.oid)
        self.assertEqual(3, len(competition.get_all_groups()))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == group.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent.oid]))
        self.assertEqual(1, len([g for g in competition.get_all_groups() if g.oid == parent_parent.oid]))


class TestCompConfiguratorTeams(BaseTeamTestCase):

    def test_should_fail_competition_no_created(self):
        with pytest.raises(DomainError, match="Competition has to exist before the teams and rankings can be setup."):
            CompetitionConfigurator.process_competition_team_configuration(None, None)

    def test_should_fail_no_team_configuration(self):
        with pytest.raises(DomainError, match="No team configuration given."):
            competition = create_default_competition_for_testing("My Comp")
            CompetitionConfigurator.process_competition_team_configuration(None, competition)

    def test_should_fail_group_not_created(self):
        with pytest.raises(DomainError, match="Group Team Group 1 has not been created yet."):
            competition = create_default_competition_for_testing("My Comp")
            sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
            comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp_config, None, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

    def test_should_fail_too_many_groups(self):
        with pytest.raises(DomainError, match="Group with name: Group_First appears more than once: 2."):
            competition = create_default_competition_for_testing("My Comp")
            sub_comp = TableSubCompetition("My Sub Comp", None, competition, [], 1, False, False, False, False)

            comp_group_config = CompetitionGroupConfiguration("Group_First", sub_comp, None, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE, 1, None)

            comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
            sub_comp.groups.append(comp_group)

            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

    def test_should_fail_too_many_teams(self):
        with pytest.raises(DomainError, match=r"Team My Team has too many 2 teams created."):
            competition = create_default_competition_for_testing("My Comp")
            sub_comp = TableSubCompetition("My Sub Comp", None, competition, [], 1, False, False, False, False)

            comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp, None, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE, 1, None)

            comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
            team = Team("My Team", 5, True)
            competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
            comp_team = CompetitionTeam(competition, team)
            competition.teams = [comp_team, comp_team]
            CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

    def test_should_add_team_team_does_not_exist(self):
        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)

        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, sub_comp, comp_group_config, 1, None)
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

        self.assertEqual(1, len(competition.teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(team.oid, comp_group.rankings[0].team.parent_team.oid)

    def test_should_add_team_team_exists(self):
        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", None, competition, [], 1, False, False, False, False)

        comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp, None, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)

        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        competition.teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

        self.assertEqual(1, len(competition.teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)

    def test_should_add_team_multiple_parents(self):
        competition = create_default_competition_for_testing("My Comp", 3)
        sub_comp = TableSubCompetition("My Sub Comp", None, competition, [], 1, False, False, False, False)

        parent_comp_group_config = CompetitionGroupConfiguration("Parent Group 1", sub_comp, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp, parent_comp_group_config, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)

        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        self.assertEqual(2, len(competition.get_all_groups()))
        team = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        competition.teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)

        self.assertEqual(1, len(competition.teams))
        self.assertEqual(1, len(comp_group.rankings))
        self.assertEqual(1, len(comp_group.parent_group.rankings))
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)
        self.assertEqual(comp_team.oid, comp_group.parent_group.rankings[0].team.oid)

    def test_should_add_multiple_teams(self):
        competition = create_default_competition_for_testing("My Comp")
        sub_comp = TableSubCompetition("My Sub Comp", [], competition, [], 1, False, False, False, False)

        parent_comp_group_config = CompetitionGroupConfiguration("Parent Group 1", sub_comp, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        comp_group_config = CompetitionGroupConfiguration("Team Group 1", sub_comp, parent_comp_group_config, 1,
                                                          CompetitionGroupConfiguration.RANKING_TYPE, 1, None)
        comp_group = CompetitionConfigurator.create_competition_group(comp_group_config, competition)
        self.assertEqual(2, len(competition.get_all_groups()), "Get all groups")
        team = Team("My Team", 5, True)
        team2 = Team("My Team", 5, True)
        competition_team_configuration = CompetitionTeamConfiguration(team, None, comp_group_config, 1, None)
        competition_team_configuration2 = CompetitionTeamConfiguration(team2, None, comp_group_config, 1, None)
        comp_team = CompetitionTeam(competition, team)
        competition.teams = [comp_team]
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration, competition)
        CompetitionConfigurator.process_competition_team_configuration(competition_team_configuration2, competition)

        self.assertEqual(2, len(competition.teams), "teams")
        self.assertEqual(2, len(comp_group.rankings), "rankings")
        self.assertEqual(2, len(comp_group.parent_group.rankings), "parent rankings")
        self.assertEqual(comp_team.oid, comp_group.rankings[0].team.oid)
        self.assertEqual(comp_team.oid, comp_group.parent_group.rankings[0].team.oid)
        self.assertEqual(competition.teams[1].oid, comp_group.rankings[1].team.oid)
        self.assertEqual(competition.teams[1].oid, comp_group.parent_group.rankings[1].team.oid)


class TestCompConfiguratorTableGames(BaseTeamTestCase):

    @mark.notwritten
    def test_should_process_table_game(self):
        # need multiple types
        pass


class TestCompConfiguratorSeriesGames(BaseTeamTestCase):

    def test_should_process_comp_series_no_sub_comp(self):
        with pytest.raises(DomainError,
                           match="Sub Competition must be created before competition games can be processed."):
            sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
            series = CompetitionConfigurator.process_series_configuration(
                SeriesConfiguration("Series 1", 5, None,
                                    CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None),
                                    1,
                                    CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None),
                                    2,
                                    SeriesByGoalsRules("My Rules", 5, sub_comp_config, None, None), None,
                                    CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None),
                                    1, None),
                None)

    def test_should_process_comp_series_no_comp(self):
        with pytest.raises(DomainError, match="Competition must be created before competition games can be processed."):
            sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
            sub_comp = PlayoffSubCompetition("test", [], None, None, 1, 1, False, False, False, False)
            sub_comp.groups = [
                CompetitionGroup("Group 1", None, None, None, None, None),
                CompetitionGroup("Group 3", None, None, None, None, None),
                CompetitionGroup("Group 4", None, None, None, None, None),
            ]
            series = CompetitionConfigurator.process_series_configuration(
                SeriesConfiguration("Series 1", 5, sub_comp,
                                    CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None),
                                    1,
                                    CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None),
                                    2,
                                    SeriesByGoalsRules("My Rules", 5, None, None, None), None,
                                    CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None),
                                    CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None),
                                    1, None),
                sub_comp)

    def test_should_process_by_goals_method(self):
        sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
        group1 = CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None)
        group3 = CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None)
        group4 = CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None)
        series = CompetitionConfigurator.process_series_by_goals_configuration(
            SeriesConfiguration("Series 1", 5, None,
                                group1, 1,
                                group1, 2,
                                SeriesByGoalsRules("My Rules", 5, None, None, None),
                                group3,
                                group4,
                                group3,
                                group4,
                                1, None),
            [group1, group3, group4],
            None)

        self.assertEqual("Series 1", series.name)
        self.assertEqual("Group 1", series.home_team_from_group.name)
        self.assertEqual("Group 1", series.away_team_from_group.name)
        self.assertEqual("Group 3", series.winner_to_group.name)
        self.assertEqual("Group 3", series.loser_to_group.name)
        self.assertEqual("Group 4", series.winner_rank_from.name)
        self.assertEqual("Group 4", series.loser_rank_from.name)

    def test_should_process_by_goals_method_wrong_rules(self):
        with pytest.raises(DomainError, match="Series My Configuration does not have the correct rules."):
            series = CompetitionConfigurator.process_series_by_goals_configuration(
                SeriesConfiguration("My Configuration", 5, None, None, None, None,
                                    None, SeriesByWinsRules("Test Rules", 4, None, None), None,
                                    None, None, None, None, 1, None),
                None, None)

    # TODO: should handle a None comp group configuration
    def test_should_process_by_wins_method(self):
        competition = create_default_competition_for_testing("Test", 1)
        sub_comp = PlayoffSubCompetition("Test", [], competition, [], 1, 1, False, False, False, False)

        sub_comp_config = SubCompetitionConfiguration("Test", None, None, None, None, None, None, None, None)
        group1 = CompetitionGroupConfiguration("Group 1", sub_comp_config, None, 1, None, 1, None)
        group3 = CompetitionGroupConfiguration("Group 3", sub_comp_config, None, 1, None, 1, None)
        group4 = CompetitionGroupConfiguration("Group 4", sub_comp_config, None, 1, None, 1, None)

        sub_comp.groups = [
            CompetitionConfigurator.create_competition_group(group1, competition),
            CompetitionConfigurator.create_competition_group(group3, competition),
            CompetitionConfigurator.create_competition_group(group4, competition)
        ]
        series = CompetitionConfigurator.processes_series_by_wins_configuration(
            SeriesConfiguration("Series 1", 5, None,
                                group1, 1,
                                group1, 2,
                                SeriesByWinsRules("My Rules", 4, None, None, None),
                                group3,
                                group4,
                                group3,
                                group4,
                                1, None),
            sub_comp)

        self.assertEqual("Series 1", series.name)
        self.assertEqual("Group 1", series.home_team_from_group.name)
        self.assertEqual("Group 1", series.away_team_from_group.name)
        self.assertEqual("Group 3", series.winner_to_group.name)
        self.assertEqual("Group 3", series.loser_to_group.name)
        self.assertEqual("Group 4", series.winner_rank_from.name)
        self.assertEqual("Group 4", series.loser_rank_from.name)

    def test_should_process_by_wins_method_wrong_rules(self):
        with pytest.raises(DomainError, match="Series My Configuration does not have the correct rules."):
            series = CompetitionConfigurator.processes_series_by_wins_configuration(
                SeriesConfiguration("My Configuration", 5, None, None, None, None,
                                    None, SeriesByGoalsRules("Test Rules", 4, None, None, None), None,
                                    None, None, None, None, 1, None),
                None)

    def test_should_process_series_game_config(self):
        playoff_comp_config = PlayoffSubCompetitionConfiguration("Playoff Comp", None, None, [], [], 1, 1, None)
        group1 = CompetitionGroupConfiguration("Group 1", playoff_comp_config, None, 1, None, 1, None)
        group3 = CompetitionGroupConfiguration("Group 3", playoff_comp_config, None, 1, None, 1, None)
        group4 = CompetitionGroupConfiguration("Group 4", playoff_comp_config, None, 1, None, 1, None)
        series_config = SeriesConfiguration("Series 1", 5, playoff_comp_config,
                                            group1, 1,
                                            group1, 2,
                                            SeriesByWinsRules("My Rules", 5, None, None, None), None,
                                            group3, group4,
                                            group3, group4,
                                            1, None)

        competition = create_default_competition_for_testing("My Comp", 1)
        playoff_comp = PlayoffSubCompetition("Playoff Comp", [], competition, [], None, None, None, None, None, None)

        CompetitionConfigurator.process_series_configuration(series_config, playoff_comp)

        self.assertEqual(1, len(competition.sub_competitions[0].series_configurations))
        new_series = competition.sub_competitions[0].series_configurations[0]
        self.assertEqual("Series 1", new_series.name)
        self.assertEqual(3, len(competition.get_all_groups()))

    def test_should_process_series_game_not_playoff_sub_comp(self):
        competition = create_default_competition_for_testing("My Comp", 1)
        with pytest.raises(DomainError, match="Sub Competition Table Comp is not a playoff sub competition."):
            CompetitionConfigurator.process_series_configuration(
                None,
                TableSubCompetition("Table Comp", None, competition, [], None, None, None, None, None)
            )
