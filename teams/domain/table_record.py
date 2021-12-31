# mapped
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.domain.record import Record


class TableRecord(Record):
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("TableSubCompetition", foreign_keys=[sub_competition_id])

    __mapper_args__ = {
        'polymorphic_identity': 'table_record'
    }

    def __init__(self, sub_competition, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid=None):
        self.sub_competition = sub_competition

        Record.__init__(self, rank, team, year, wins, loses, ties, goals_for, goals_against, skill, oid)
