from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_game import GameDTO
from teams.domain.competition import CompetitionGame


class CompetitionGameDTO(GameDTO, CompetitionGame):
    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("SubCompetitionDTO", foreign_keys=[sub_competition_id])
    competition_id = Column(String, ForeignKey('competitions.oid'))
    competition = relationship("CompetitionDTO", foreign_keys=[competition_id])

    __mapper_args__ = {
        'polymorphic_identity': 'competition_game'
    }

    def __init__(self, competition_game):

        CompetitionGame.__init__(self, competition_game.competition,
                                 competition_game.sub_competition,
                                 competition_game.day,
                                 competition_game.home_team,
                                 competition_game.away_team,
                                 competition_game.home_score,
                                 competition_game.away_score,
                                 competition_game.complete,
                                 competition_game.game_processed,
                                 competition_game.rules,
                                 competition_game.oid)
