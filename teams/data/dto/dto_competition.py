from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.competition import Competition
from teams.data.dto.dto_competition_game import CompetitionGameDTO


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
    games = relationship("CompetitionGameDTO", back_populates="competition")

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
