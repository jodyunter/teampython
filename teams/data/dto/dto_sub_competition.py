from abc import ABC

from teams.data.dto.dto_base import Base
from teams.domain.sub_competition import SubCompetition


class SubCompetitionDTO(ABC, Base, SubCompetition):
    __tablename__ = "subcompetitions"

    def __init__(self, sub_competition):

        SubCompetition.__init__(self,
                                sub_competition.name,
                                sub_competition.sub_competition_type,
                                sub_competition.competition,
                                sub_competition.groups,
                                sub_competition.order,
                                sub_competition.setup,
                                sub_competition.started,
                                sub_competition.finished,
                                sub_competition.post_processed,
                                sub_competition.oid)