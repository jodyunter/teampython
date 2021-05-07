from sqlalchemy import Column, String, Integer, Boolean

from teams.data.dto.dto_base import Base
from teams.domain.competition import Competition


class CompetitionDTO(Base, Competition):
    __tablename__ = "competitions"

    oid = Column(String, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    current_round = Column(Integer)
    setup = Column(Boolean)
    started = Column(Boolean)
    finished = Column(Boolean)
    post_processed = Column(Boolean)

    def __init__(self, competition):

        Competition.__init__(self, competition.name,
                             competition.year,
                             competition.sub_competitions,
                             competition.teams,
                             competition.current_round,
                             competition.setup,
                             competition.started,
                             competition.finished,
                             competition.post_processed,
                             competition.oid)

    def __eq__(self, other):
        return self.oid == other.oid and \
            self.name == other.name and \
            self.current_round == other.current_round and \
            self.setup == other.setup and \
            self.started == other.started and \
            self.finished == other.finished and \
            self.post_processed == other.post_processed

