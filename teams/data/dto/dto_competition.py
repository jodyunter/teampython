from teams.data.dto.dto_base import Base
from teams.domain.competition import Competition


class CompetitionDTO(Base, Competition):
    __tablename__ = "Competitions"

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
