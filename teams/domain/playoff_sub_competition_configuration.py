from sqlalchemy.orm import relationship

from teams.domain.sub_competition_configuration import SubCompetitionConfiguration


class PlayoffSubCompetitionConfiguration(SubCompetitionConfiguration):
    __mapper_args__ = {
        'polymorphic_identity': 'playoff_sub_competition_configuration'
    }

    series_configurations = relationship("SeriesConfiguration", back_populates="sub_competition_configuration")

    def __init__(self, name, competition_configuration, competition_group_configs,
                 series_configs, order, first_year, last_year, oid=None):
        self.series_configurations = series_configs

        SubCompetitionConfiguration.__init__(self, name, competition_configuration,
                                             competition_group_configs, order, SubCompetitionConfiguration.PLAYOFF_TYPE,
                                             first_year, last_year, oid)
