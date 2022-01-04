from sqlalchemy import Integer, Column

from teams.domain.series_rules import SeriesRules


class SeriesByWinsRules(SeriesRules):
    required_wins = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'series_by_wins_rules'
    }

    def __init__(self, name, required_wins, game_rules, home_pattern, oid=None):
        self.required_wins = required_wins

        SeriesRules.__init__(self, name, game_rules, SeriesRules.WINS_TYPE, home_pattern, oid)
