#  create the competition
#  create the groups
#  create the teams
#  create the rankings
#  create the sub competions
#     create the series or records
#  create the games for the first sub competitions
#  schedule the games
#  everytime a playoff game is done, check if you need to schedule for for that series
#  everytime a playoff series is done, check if the round is done, if it's done, go to the next round
#  a playoff series sub competition can be done in order, and from groups create by previous rounds
#  so if you want a playoff round to run at the same time as a table, but the second round is after, it's another sub competition
#  all sub competitions must be done before we can go onto the next order of sub comps
#  all sub comps should be created at the same time but not setup until their order comes up so that we can rely on groups populated by previouis comps
import uuid

from teams.domain.competition import Competition, SubCompetition
from teams.domain.competition_configuration import CompetitionConfiguration

comp_config = CompetitionConfiguration("My Comp", 1, 1, None, uuid.uuid4())


def create_competition_from_config(competition_config, year):
    return Competition(competition_config.name, year, False, False, False, False, uuid.uuid4())


def create_sub_competition_fromConfig(sub_competition_config, competition):
    return SubCompetition(sub_competition_config.name, sub_competition_config.sub_competition_type,
                          competition, False, False, False, False, uuid.uuid4())


def create_competition_group_from_config(competition_group_config, ):
    return

