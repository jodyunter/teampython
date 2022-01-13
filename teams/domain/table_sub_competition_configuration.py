from teams.domain.sub_competition_configuration import SubCompetitionConfiguration


class TableSubCompetitionConfiguration(SubCompetitionConfiguration):
    __mapper_args__ = {
        'polymorphic_identity': 'table_sub_competition_configuration'
    }

    def __init__(self, name, competition_configuration, competition_team_configs, order,
                 first_year, last_year, oid=None):

        SubCompetitionConfiguration.__init__(self, name, competition_configuration,
                                             competition_team_configs, order, SubCompetitionConfiguration.TABLE_TYPE,
                                             first_year, last_year, oid)