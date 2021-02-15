from unittest import TestCase

from pytest import mark

from teams.domain.sub_competition import TableSubCompetition
from tests.teams.domain.competition import helpers


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

    @mark.notwritten
    def test_sort_rankings(self):
        pass
