import uuid

from sqlalchemy import String, Integer, Column

from teams.data.dto.dto_base import Base
from teams.domain.team import Team


class TeamDTO(Base, Team):
    __tablename__ = "teams"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    skill = Column(Integer, default=5)

    def __init__(self, team):
        Team.__init__(self, team.name, team.skill, team.oid)

    @staticmethod
    def get_dto(team):
        if not team.__class__ == TeamDTO:
            team_dto = TeamDTO(team)
        else:
            team_dto = team

        return team_dto

