import uuid

from sqlalchemy import String, Integer, Column

from teams.data.dto.dto_base import Base
from teams.domain.team import Team


class TeamDTO(Base, Team):
    __tablename__ = "teams"

    oid = Column(String, primary_key=True)
    name = Column(String, default="None")
    skill = Column(Integer, default=5)

    def __init__(self, name, skill, oid=str(uuid.uuid4())):
        self.oid = oid
        self.name = name
        self.skill = skill

