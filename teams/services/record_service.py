from teams.data.dto.dto_record import RecordDTO
from teams.data.repo.record_repository import RecordRepository
from teams.data.repo.team_repository import TeamRepository
from teams.services.base_service import BaseService
from teams.services.view_models.team_views import RecordView


class RecordService(BaseService):
    repo = RecordRepository()
    team_repo = TeamRepository()

    def add(self, team_view_list, year):
        session = self.repo.get_session()
        team_list = [self.team_repo.get_by_oid(t.oid, session) for t in team_view_list]
        record_list = [RecordDTO(t, year, 0, 0, 0, 0, 0, self.get_new_id()) for t in team_list]
        [self.repo.add(r, session) for r in record_list]
        session.commit()

    def update_records(self, updated_records):
        [self.update_record(r.oid, r.team_id, r.wins, r.loses, r.ties, r.goals_for, r.goals_against)
         for r in updated_records]

    def update_record(self, oid, team_id, wins, loses, ties, goals_for, goals_against):
        session = self.repo.get_session()
        team_dto = self.team_repo.get_by_oid(team_id, session)
        record_dto = self.repo.get_by_oid(oid, session)
        record_dto.team = team_dto
        record_dto.wins = wins
        record_dto.loses = loses
        record_dto.ties = ties
        record_dto.goals_for = goals_for
        record_dto.goals_against = goals_against
        session.commit()

    def get_by_year(self, year):
        session = self.repo.get_session()
        view_list = [RecordView(r.oid, r.team.oid, r.team.name, r.year, r.wins,
                                r.loses, r.ties, r.goals_for, r.goals_against, r.points, r.games)
                     for r in self.repo.get_by_year(year, session)]
        return view_list

    def get_by_year_range(self, first_year, last_year):
        raise NotImplementedError

    def get_by_team(self, team_id):
        raise NotImplementedError
