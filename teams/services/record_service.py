from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.services.base_service import BaseService
from teams.services.view_models.team_view_models import RecordViewModel


class RecordService(BaseService):
    repo = RecordRepository()
    team_repo = TeamRepository()

    def add(self, team_view_list, year, session=None):
        commit = session is None
        session = self.get_session(session)
        team_list = [self.team_repo.get_by_oid(t.oid, session) for t in team_view_list]
        record_list = [Record(-1, t, year, 0, 0, 0, 0, 0, self.get_new_id()) for t in team_list]
        [self.repo.add(r, session) for r in record_list]
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

        team = self.team_repo.get_by_oid(team_id, session)
        record = self.repo.get_by_oid(oid, session)
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

        result = list(self.repo.get_by_year(year, session))
        result.sort(key=lambda rec: (-rec.points, -rec.wins, rec.games, -rec.goal_difference))

        rank = 1
        for r in result:
            r.rank = rank
            rank += 1

        self.update_records(result)

        self.commit(session, commit)

    def get_by_year(self, year):
        session = self.get_session()
        view_list = [RecordViewModel(r.oid, r.rank, r.team.oid, r.team.name, r.year, r.wins,
                                     r.loses, r.ties, r.goals_for, r.goals_against, r.points, r.games,
                                     r.goal_difference, r.team.skill)
                     for r in self.repo.get_by_year(year, session)]

        return view_list

    def get_by_team_and_year(self, team_id, year, session=None):
        session = self.get_session(session)
        return self.repo.get_by_team_and_year(team_id, year, session)