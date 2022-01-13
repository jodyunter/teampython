# mapped
from sqlalchemy import String, Column, Boolean

from teams.domain.base import Base
from teams.domain.utility.utility_classes import IDHelper


class GameRules(Base):
    __tablename__ = "GameRules"

    oid = Column(String, primary_key=True)
    name = Column(String, unique=True)
    can_tie = Column(Boolean)

    def __init__(self, name, can_tie, oid=None):
        self.oid = IDHelper.get_id(oid)
        self.name = name
        self.can_tie = can_tie

    def __eq__(self, other):
        return self.name == other.name and self.can_tie == other.can_tie and self.oid == other.oid
