from abc import ABC, abstractmethod

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from teams.domain.base import Base
from teams.domain.utility.utility_classes import IDHelper


# mapped
class SubCompetition(Base, ABC):
    __tablename__ = "SubCompetitions"

    oid = Column(String, primary_key=True)
    name = Column(String)
    sub_competition_type = Column(String)
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("Competition", foreign_keys=[competition_id], back_populates="sub_competitions")
    groups = relationship("CompetitionGroup", back_populates="sub_competition")
    order = Column(Integer)
    setup = Column(Boolean)
    started = Column(Boolean)
    finished = Column(Boolean)
    post_processed = Column(Boolean)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'sub_competition'
    }

    def __init__(self, name, sub_competition_type, competition, groups, order, setup, started, finished, post_processed,
                 oid=None):
        self.name = name
        self.sub_competition_type = sub_competition_type
        self.competition = competition
        self.order = order
        self.setup = setup
        self.started = started
        self.finished = finished
        self.post_processed = post_processed
        if groups is None:
            self.groups = []
        else:
            self.groups = groups
        if oid is None:
            self.oid = IDHelper.get_id(oid)
        else:
            self.oid = oid

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def process_game(self, game):
        pass

    @abstractmethod
    def create_new_games(self, **kwargs):
        pass

    @abstractmethod
    def is_complete(self, **kwargs):
        pass

    @abstractmethod
    def post_process(self, **kwargs):
        pass

    @abstractmethod
    def process_end_of_day(self):
        pass

    def get_groups_by_level(self, level):
        return [g for g in self.groups if g.level == level]

    def get_group_by_name(self, name):
        groups = [g for g in self.groups if g.name == name]
        if groups is None or len(groups) == 0:
            return []
        else:
            return groups[0]

    def __eq__(self, other):
        return self.oid == other.oid and \
            self.name == other.name and \
            self.sub_competition_type == other.sub_competition_type and \
            self.competition == other.competition and \
            self.order == other.order and \
            self.setup == other.setup and \
            self.started == other.started and \
            self.finished == other.finished and \
            self.post_processed == other.post_processed
