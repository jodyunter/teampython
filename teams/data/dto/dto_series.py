from sqlalchemy import ForeignKey, String, Column, Integer, Boolean
from sqlalchemy.orm import relationship

from teams.data.dto.dto_base import Base
from teams.domain.series import Series


class SeriesDTO(Base, Series):
    __tablename__ = "series"

    sub_competition_id = Column(String, ForeignKey('subcompetitions.oid'))
    sub_competition = relationship("TableSubCompetitionDTO", foreign_keys=[sub_competition_id])
    name = Column(String)
    series_round = Column(Integer)
    home_team_id = Column(String, ForeignKey('teams.oid'))
    home_team = relationship("TeamDTO", foreign_keys=[home_team_id])
    away_team_id = Column(String, ForeignKey('teams.oid'))
    away_team = relationship("TeamDTO", foreign_keys=[away_team_id])
    series_type = Column(String)
    series_rules_id = Column(String, ForeignKey('seriesrules.oid'))
    series_rules = relationship("SeriesRulesDTO", foreign_keys=[series_rules_id])
    home_team_from_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    home_team_from_group = relationship("CompetitionGroupDTO", foreign_keys=[home_team_from_group_id])
    home_team_value = Column(Integer)
    away_team_from_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    away_team_from_group = relationship("CompetitionGroupDTO", foreign_keys=[away_team_from_group_id])
    away_team_value = Column(Integer)
    winner_to_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    winner_to_group = relationship("CompetitionGroupDTO", foreign_keys=[winner_to_group_id])
    loser_to_group_id = Column(String, ForeignKey('competitiongroup.oid'))
    loser_to_group = relationship("CompetitionGroupDTO", foreign_keys=[loser_to_group_id])
    setup = Column(Boolean)
    post_processed = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'series'
    }

    def __init__(self, series):

        Series.__init__(self,
                        series.sub_competition,
                        series.name,
                        series.series_round,
                        series.home_team,
                        series.away_team,
                        series.series_type,
                        series.series_rules,
                        series.home_team_from_group,
                        series.home_team_value,
                        series.away_team_from_group,
                        series.away_team_value,
                        series.winner_to_group,
                        series.winner_rank_from,
                        series.loser_to_group,
                        series.loser_rank_from,
                        series.setup,
                        series.post_processed,
                        series.oid)