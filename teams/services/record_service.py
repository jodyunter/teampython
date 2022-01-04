from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.services.base_service import BaseService
from teams.services.view_models.team_view_models import RecordViewModel


class RecordService(BaseService):
    team_repo = TeamRepository()
    repo = RecordRepository()

    def get_team_repo(self):
        return self.team_repo

    def get_repo(self):
        return self.repo

    def add(self, team_view_list, year, session=None):
        commit = session is None
        session = self.get_session(session)
        team_list = [self.get_team_repo().get_by_oid(t.oid, session) for t in team_view_list]
        record_list = [Record(-1, t, year, 0, 0, 0, 0, 0, t.skill, self.get_new_id()) for t in team_list]
        [self.get_repo().add(r, session) for r in record_list]
        self.commit(session, commit)

    def update_records(self, updated_records, session=None):
        commit = session is None
        session = self.get_session(session)

        [self.update_record(r.oid, r.team_id, r.wins, r.loses, r.ties, r.goals_for, r.goals_against, session)
         for r in updated_records]

        self.commit(session, commit)

    def update_record(self, oid, team_id, wins, loses, ties, goals_for, goals_against, session=None):
        commit = session is None
        session = self.get_session(session)
        repo = self.get_repo()
        team_repo = self.get_team_repo()
        team = team_repo.get_by_oid(team_id, session)
        record = repo.get_by_oid(oid, session)
        record.team = team
        record.wins = wins
        record.loses = loses
        record.ties = ties
        record.goals_for = goals_for
        record.goals_against = goals_against
        self.commit(session, commit)

    def update_rank(self, year, session=None):
        commit = session is None
        session = self.get_session(session)
        repo = self.get_repo()
        result = list(repo.get_by_year(year, session))
        result.sort(key=lambda rec: (-rec.points, -rec.wins, rec.games, -rec.goal_difference))

        rank = 1
        for r in result:
            r.rank = rank
            rank += 1

        self.update_records(result, session)

        self.commit(session, commit)

    def get_by_year(self, year):
        session = self.get_session()
        repo = self.get_repo()
        view_list = [self.get_view_from_model(r)
                     for r in repo.get_by_year(year, session)]

        return view_list

    @staticmethod
    def get_view_from_model(r, rank=None):
        if r is None:
            return None
        if rank is None:
            rank = r.rank
        return RecordViewModel(r.oid, rank, r.team.oid, r.team.name, r.year, r.wins,
                               r.loses, r.ties, r.goals_for, r.goals_against, r.points, r.games,
                               r.goal_difference, r.skill)

    def get_by_team_and_year(self, team_id, year, session=None):
        session = self.get_session(session)
        repo = self.get_repo()
        return RecordService.get_view_from_model(repo.get_by_team_and_year(team_id, year, session))

    def get_by_team(self, team_id, session=None):
        session = self.get_session(session)
        repo = self.get_repo()
        return [RecordService.get_view_from_model(r) for r in repo.get_by_team(team_id, session)]

    def get_all_by_rank(self, rank, session=None):
        session = self.get_session(session)
        repo = self.get_repo()
        return [RecordService.get_view_from_model(r) for r in repo.get_by_rank(rank, session)]

    @staticmethod
    def sort_default(standings):
        reverse = False        
        standings.sort(key=lambda rec: rec.rank, reverse=reverse)

    @staticmethod
    def sort_by_year(standings):
        standings.sort(key=lambda rec: rec.year)

    def get_all_seasons_for_dropdown(self):
        repo = self.get_repo()
        session = self.get_session()
        data = repo.get_list_of_seasons(session)
        return [a.year for a in data]
