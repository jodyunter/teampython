from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.domain.record import Record
from teams.services.base_service import BaseService
from teams.services.view_models.team_view_models import RecordViewModel


class RecordService(BaseService):
    repo = RecordRepository()
    team_repo = TeamRepository()

    def add(self, team_view_list, year):
        session = self.repo.get_session()
        team_list = [self.team_repo.get_by_oid(t.oid, session) for t in team_view_list]
        record_list = [Record(t, year, 0, 0, 0, 0, 0, self.get_new_id()) for t in team_list]
        [self.repo.add(r, session) for r in record_list]
        session.commit()

    def update_records(self, updated_records, session=None):
        if session is None:
            session = self.repo.get_session()
        [self.update_record(r.oid, r.team_id, r.wins, r.loses, r.ties, r.goals_for, r.goals_against, session)
         for r in updated_records]

        session.commit

    def update_record(self, oid, team_id, wins, loses, ties, goals_for, goals_against, session=None):
        commit = False
        if session is None:
            session = self.repo.get_session()
            commit = True

        team = self.team_repo.get_by_oid(team_id, session)
        record = self.repo.get_by_oid(oid, session)
        record.team = team
        record.wins = wins
        record.loses = loses
        record.ties = ties
        record.goals_for = goals_for
        record.goals_against = goals_against
        if commit:
            session.commit()

    def get_by_year(self, year):
        session = self.repo.get_session()
        view_list = [RecordViewModel(r.oid, r.team.oid, r.team.name, r.year, r.wins,
                                     r.loses, r.ties, r.goals_for, r.goals_against, r.points, r.games,
                                     r.goal_difference)
                     for r in self.repo.get_by_year(year, session)]
        return view_list

    def get_by_team_and_year(self, team_id, year, session=None):
        if session is None:
            session = self.repo.get_session()
        return self.repo.get_by_team_and_year(team_id, year, session)

    def get_by_year_range(self, first_year, last_year):
        raise NotImplementedError

    def get_by_team(self, team_id):
        raise NotImplementedError
