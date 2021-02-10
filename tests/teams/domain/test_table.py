from unittest import TestCase
from teams.domain.table_competition import TableRanking, TableRecord, TableCompetition, TableDivision
from teams.domain.team import Team


class TestTable(TestCase):

    def test_should_sort_by_ranking(self):
        table_division = TableDivision(None, "Div 1", None, 1, 1)
        table_rankings = [
            TableRanking(TableRecord(None, -1, Team("Team 1", 5, False, -1), 5, 12, 0, 0, 0, 0, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 2", 5, False, -1), 5, 10, 0, 2, 0, 0, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 3", 5, False, -1), 5, 11, 1, 0, 0, 0, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 4", 5, False, -1), 5, 12, 5, 0, 0, 0, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 5", 5, False, -1), 5, 0, 0, 5, 5, 15, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 6", 5, False, -1), 5, 0, 0, 5, 5, 5, 5, -1), table_division, -1),
            TableRanking(TableRecord(None, -1, Team("Team 7", 5, False, -1), 5, 0, 0, 5, 10, 5, 5, -1), table_division, -1)
        ]

        TableCompetition.sort_records_by_division(table_rankings)

        ranking = [a for a in table_rankings if a.rank == 1]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 1", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 2]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 4", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 3]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 3", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 4]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 2", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 5]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 7", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 6]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 6", ranking[0].record.team.name)

        ranking = [a for a in table_rankings if a.rank == 7]
        self.assertEqual(1, len(ranking))
        self.assertEqual("Team 5", ranking[0].record.team.name)