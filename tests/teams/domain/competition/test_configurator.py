from unittest import TestCase

import pytest

from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition import Competition
from teams.domain.competition_configuration import SubCompetitionConfiguration, CompetitionGroupConfiguration
from teams.domain.errors import DomainError
from teams.domain.sub_competition import SubCompetition, TableSubCompetition


class TestCompConfigurator(TestCase):

    def test_should_create_group_group_already_setup(self):
        raise NotImplementedError

    def test_should_not_create_group_competition_not_there(self):
        with pytest.raises(DomainError, match="Competition has to exist before the groups can be setup."):
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                          None)
            comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                     CompetitionGroupConfiguration.RANKING_TYPE,
                                                                     1, None)
            comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config, 1,
                                                              CompetitionGroupConfiguration.RANKING_TYPE,
                                                              1, None)
            current_groups = []
            group = CompetitionConfigurator.create_competition_group(comp_group_config, current_groups, None)

    def test_should_not_create_group_sub_competition_does_not_exist(self):
        with pytest.raises(DomainError, match="You are setting up groups before sub competitions."):
            sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                          None)
            comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                     CompetitionGroupConfiguration.RANKING_TYPE,
                                                                     1, None)
            comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config, 1,
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

    def test_should_create_group_parent_not_created(self):
        sub_comp_config = SubCompetitionConfiguration("My Sub Comp", None, 1, SubCompetitionConfiguration.TABLE_TYPE, 1,
                                                      None)
        comp_parent_group_config = CompetitionGroupConfiguration("Parent 1 Config", sub_comp_config, None, 1,
                                                                 CompetitionGroupConfiguration.RANKING_TYPE,
                                                                 1, None)
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config, 1,
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
        comp_group_config = CompetitionGroupConfiguration("Group 1 Config", sub_comp_config, comp_parent_group_config, 1,
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
        raise NotImplementedError

    def test_should_create_group_top_parent_exists_middle_does_not(self):
        raise NotImplementedError
