from unittest import TestCase

from teams.domain.competition_configuration import CompetitionGroupConfiguration
from teams.domain.sub_competition import TableSubCompetition, CompetitionGroup
from teams.domain.table_record import TableRecord
from tests.teams.domain.competition import helpers
from tests.teams.domain.competition.helpers import create_default_competition_for_testing


class TestTableSubCompetition(TestCase):

    def test_get_dictionary_of_team_records(self):
        comp_records = [
            helpers.new_table_record(None, "Team 1", 5),
            helpers.new_table_record(None, "Team 2", 5),
            helpers.new_table_record(None, "Team 3", 5),
            helpers.new_table_record(None, "Team 4", 5),
            helpers.new_table_record(None, "Team 5", 5),
            helpers.new_table_record(None, "Team 6", 5),
            helpers.new_table_record(None, "Team 7", 5),
        ]

        team_map = TableSubCompetition.get_dictionary_of_team_records(comp_records)
        self.assertEqual(7, len(team_map))
        self.assertTrue(comp_records[0].team.oid in team_map)

    def test_sort_rankings(self):
        competition = create_default_competition_for_testing("My Comp")
        table = TableSubCompetition("My Table", [], None, None, 1, False, False, False, False)
        competition.sub_competitions.append(table)

        teams = [
            helpers.new_comp_team(competition, "Team 1", 5),
            helpers.new_comp_team(competition, "Team 2", 5),
            helpers.new_comp_team(competition, "Team 3", 5),
            helpers.new_comp_team(competition, "Team 4", 5),
            helpers.new_comp_team(competition, "Team 5", 5),
            helpers.new_comp_team(competition, "Team 6", 5),
            helpers.new_comp_team(competition, "Team 7", 5),
            helpers.new_comp_team(competition, "Team 8", 5)
        ]

        records = [
            TableRecord(table, -1, teams[0], 255, 10, 0, 0, 0, 0, 0, ""),
            TableRecord(table, -1, teams[1], 255, 9, 0, 2, 0, 0, 0, ""),
            TableRecord(table, -1, teams[2], 255, 6, 2, 2, 0, 0, 0, ""),
            TableRecord(table, -1, teams[3], 255, 7, 3, 0, 0, 0, 0, ""),
            TableRecord(table, -1, teams[4], 255, 0, 0, 4, 12, 12, 0, ""),
            TableRecord(table, -1, teams[5], 255, 0, 0, 4, 6, 12, 0, ""),
            TableRecord(table, -1, teams[6], 255, 0, 0, 4, 12, 6, 0, ""),
            TableRecord(table, -1, teams[7], 255, 0, 10, 0, 12, 6, 0, "")
        ]

        table.records = records

        group1 = CompetitionGroup("League", None, table, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        group2 = CompetitionGroup("East", None, table, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)
        group3 = CompetitionGroup("West", None, table, 1, [], CompetitionGroupConfiguration.RANKING_TYPE)

        [group1.add_team_to_group(t) for t in teams]
        for i in range(len(records)):
            if i % 2 == 0:
                group2.add_team_to_group(teams[i])
            else:
                group3.add_team_to_group(teams[i])

        self.assertEqual(8, len(group1.rankings))
        self.assertEqual(4, len(group2.rankings))
        self.assertEqual(4, len(group3.rankings))

        rankings = []
        rankings.extend(group1.rankings)
        rankings.extend(group2.rankings)
        rankings.extend(group3.rankings)

        table.sort_rankings(rankings, records)

        self.assertEqual("Team 1", records[0].team.name)
        self.assertEqual("Team 2", records[1].team.name)
        self.assertEqual("Team 4", records[2].team.name)
        self.assertEqual("Team 3", records[3].team.name)
        self.assertEqual("Team 7", records[4].team.name)
        self.assertEqual("Team 5", records[5].team.name)
        self.assertEqual("Team 6", records[6].team.name)
        self.assertEqual("Team 8", records[7].team.name)

        self.assertEqual("Team 1", group1.get_team_by_rank(1).name)
        self.assertEqual("Team 2", group1.get_team_by_rank(2).name)
        self.assertEqual("Team 4", group1.get_team_by_rank(3).name)
        self.assertEqual("Team 3", group1.get_team_by_rank(4).name)
        self.assertEqual("Team 7", group1.get_team_by_rank(5).name)
        self.assertEqual("Team 5", group1.get_team_by_rank(6).name)
        self.assertEqual("Team 6", group1.get_team_by_rank(7).name)
        self.assertEqual("Team 8", group1.get_team_by_rank(8).name)

        self.assertEqual("Team 1", group2.get_team_by_rank(1).name)
        self.assertEqual("Team 3", group2.get_team_by_rank(2).name)
        self.assertEqual("Team 7", group2.get_team_by_rank(3).name)
        self.assertEqual("Team 5", group2.get_team_by_rank(4).name)
        self.assertEqual("Team 2", group3.get_team_by_rank(1).name)
        self.assertEqual("Team 4", group3.get_team_by_rank(2).name)
        self.assertEqual("Team 6", group3.get_team_by_rank(3).name)
        self.assertEqual("Team 8", group3.get_team_by_rank(4).name)
