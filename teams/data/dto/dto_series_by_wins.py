from sqlalchemy import Integer, Column

from teams.data.dto.dto_series import SeriesDTO
from teams.domain.series import SeriesByWins


# todo: create repo
class SeriesByWinsDTO(SeriesDTO, SeriesByWins):
    home_wins = Column(Integer)
    away_wins = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins'
    }

    def __init__(self, series_by_wins):
        SeriesByWins.__init__(self,
                              series_by_wins.sub_competition,
                              series_by_wins.name,
                              series_by_wins.series_round,
                              series_by_wins.home_team,
                              series_by_wins.away_team,
                              series_by_wins.home_wins,
                              series_by_wins.away_wins,
                              series_by_wins.series_rules,
                              series_by_wins.home_team_from_group,
                              series_by_wins.home_team_value,
                              series_by_wins.away_team_from_group,
                              series_by_wins.away_team_value,
                              series_by_wins.winner_to_group,
                              series_by_wins.winner_rank_from,
                              series_by_wins.loser_to_group,
                              series_by_wins.loser_rank_from,
                              series_by_wins.setup,
                              series_by_wins.post_processed,
                              series_by_wins.oid)
