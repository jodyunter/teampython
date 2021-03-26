from sqlalchemy import Integer, Column

from teams.data.dto.dto_series import SeriesDTO
from teams.domain.series import SeriesByGoals


# todo: create repo
class SeriesByGoalsDTO(SeriesDTO, SeriesByGoals):
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    games_played = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_goals'
    }

    def __init__(self, series_by_goals):
        SeriesByGoals.__init__(self,
                               series_by_goals.sub_competition,
                               series_by_goals.name,
                               series_by_goals.series_round,
                               series_by_goals.home_team,
                               series_by_goals.away_team,
                               series_by_goals.home_goals,
                               series_by_goals.away_goals,
                               series_by_goals.games_played,
                               series_by_goals.series_rules,
                               series_by_goals.home_team_from_group,
                               series_by_goals.home_team_value,
                               series_by_goals.away_team_from_group,
                               series_by_goals.away_team_value,
                               series_by_goals.winner_to_group,
                               series_by_goals.winner_rank_from,
                               series_by_goals.loser_to_group,
                               series_by_goals.loser_rank_from,
                               series_by_goals.setup,
                               series_by_goals.post_processed,
                               series_by_goals.oid)
