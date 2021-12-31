from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from teams.data.dto.dto_competition_game import CompetitionGameDTO
from teams.domain.series import SeriesGame


class SeriesGameDTO(CompetitionGameDTO, SeriesGame):
    series_id = Column(String, ForeignKey('series.oid'))
    series = relationship('SeriesDTO', foreign_keys=[series_id])
    game_number = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_game'
    }

    def __init__(self, series_game):
        SeriesGame.__init__(self, series_game.series,
                            series_game.game_number,
                            series_game.competition,
                            series_game.sub_competition,
                            series_game.day,
                            series_game.home_team,
                            series_game.away_team,
                            series_game.home_score,
                            series_game.away_score,
                            series_game.complete,
                            series_game.game_processed,
                            series_game.rules,
                            series_game.oid)
