from teams.domain import SubCompetition, CompetitionGame, CompetitionRanking, TableRecord
from teams.domain.sub_competition_configuration import SubCompetitionConfiguration


class TableSubCompetition(SubCompetition):
    __mapper_args__ = {
        'polymorphic_identity': 'table_sub_competition'
    }

    def start(self):
        pass

    def post_process(self, **kwargs):
        # do a final sort
        self.sort_table_rankings()
        # add users to any special groups (champion, division champions, or whatever)
        self.post_processed = True

    def __init__(self, name, records, competition, groups, order, setup, started, finished, post_processed, oid=None):
        if records is None:
            self.records = []
        else:
            self.records = records

        SubCompetition.__init__(self, name, SubCompetitionConfiguration.TABLE_TYPE, competition, groups, order, setup, started,
                                finished, post_processed,
                                oid)

    def process_end_of_day(self):
        pass

    def create_game(self, home, away, rules, year, day):
        return CompetitionGame(self.competition, self, day, home, away, 0, 0, False, False, rules)

    def process_game(self, game):
        if game.complete and not game.processed:
            home_record = [r for r in self.records if r.team.oid == game.home_team.oid][0]
            away_record = [r for r in self.records if r.team.oid == game.away_team.oid][0]

            home_record.process_game(game.home_score, game.away_score)
            away_record.process_game(game.away_score, game.home_score)

            game.processed = True

    # TODO:  this will need the configuration.
    # We should only create new games when previous round of sub comps is done.
    # This way the previous comps populate groups that we'll use to create games
    def create_new_games(self, **kwargs):
        return None

    def is_complete(self, **kwargs):
        incomplete_games = kwargs.get("incomplete_games", None)

        if incomplete_games is None or len(incomplete_games) == 0:
            return True
        else:
            return False

    @staticmethod
    def get_dictionary_of_team_records(records):
        team_record_dict = {}
        for r in records:
            team_record_dict[r.team.oid] = r

        return team_record_dict

    def sort_table_rankings(self):
        rankings = []
        for group in self.groups:
            rankings.extend(group.rankings)

        self.sort_rankings(rankings, self.records)

    @staticmethod
    # one day we need to be able to apply ranking rules, like top in each division or something like that
    def sort_rankings(team_rankings, records):
        #  sort the teams into their groups
        ranking_group_dict = CompetitionRanking.get_dictionary_of_groups_from_rankings(team_rankings)
        TableRecord.sort_records_default(records)
        #  sort the records with the team id as the key
        team_record_dict = TableSubCompetition.get_dictionary_of_team_records(records)

        for group_name in ranking_group_dict.keys():
            group = ranking_group_dict[group_name]
            #  set the team ranking to the same as their record ranking
            for team_ranking in group:
                team_ranking.rank = team_record_dict[team_ranking.team.oid].rank
            #  starting at 1 for the group
            group.sort(key=lambda team_rank: team_rank.rank)
            rank = 1
            for ranking in group:
                ranking.rank = rank
                rank += 1

    @staticmethod
    def get_records_by_group(ranking_group, table_records):
        return TableSubCompetition.get_records_by_team([r for r in ranking_group.rankings], table_records)

    @staticmethod
    def get_records_by_team(rankings, table_records):
        result = []
        for t in rankings:
            record = [r for r in table_records if r.team.oid == t.team.oid][0]
            record.rank = t.rank
            result.append(record)

        return result
