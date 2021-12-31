from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_competition_group import CompetitionGroupDTO
from teams.domain.sub_competition import SubCompetition


class SubCompetitionDTO(Base, SubCompetition):
    __tablename__ = "subcompetitions"

    oid = Column(String, primary_key=True)
    name = Column(String)
    sub_competition_type = Column(String)
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])
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

    def __init__(self, sub_competition):
        competition = CompetitionDTO.get_dto(sub_competition.compettiion)
        groups = [CompetitionGroupDTO.get_dto(g) for g in sub_competition.groups]

        SubCompetition.__init__(self,
                                sub_competition.name,
                                sub_competition.sub_competition_type,
                                competition,
                                groups,
                                sub_competition.order,
                                sub_competition.setup,
                                sub_competition.started,
                                sub_competition.finished,
                                sub_competition.post_processed,
                                sub_competition.oid)

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

    @staticmethod
    def get_dto(sub_competition):
        if sub_competition is None:
            return None
        elif sub_competition.__class__ == SubCompetitionDTO:
            return sub_competition
        else:
            return SubCompetitionDTO(sub_competition)

