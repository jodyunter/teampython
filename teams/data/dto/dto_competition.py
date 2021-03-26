from sqlalchemy import Column, String, Integer, Boolean

from teams.data.dto.dto_base import Base
from teams.domain.competition import Competition

# todo: create repo
class CompetitionDTO(Base, Competition):
    __tablename__ = "competitions"

    oid = Column(String, primary_key=True)
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
