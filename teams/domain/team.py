from sqlalchemy import Column, String, Boolean, Integer

from teams.data.dto.dto_base import Base
from teams.domain.utility.utility_classes import IDHelper


class Team(Base):
    __tablename__ = "teams"

    oid = Column(String, primary_key=True)
    name = Column(String)
    skill = Column(Integer, default=5)
    active = Column(Boolean, default=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'team'
    }

    def __init__(self, name, skill, active, oid=None):
        self.name = name
        self.skill = skill
        self.active = active
        self.oid = IDHelper.get_id(oid)

    def __eq__(self, other):
        return self.name == other.name and \
               self.active == other.active and \
               self.skill == other.skill and \
               self.oid == other.oid
