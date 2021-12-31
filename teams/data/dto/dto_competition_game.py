from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from teams.data.dto.dto_competition import CompetitionDTO
from teams.data.dto.dto_competition_team import CompetitionTeamDTO
from teams.data.dto.dto_game import GameDTO
from teams.data.dto.dto_game_rules import GameRulesDTO
from teams.data.dto.dto_sub_competition import SubCompetitionDTO
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
        competition = CompetitionDTO.get_dto(competition_game.competition)
        sub_competition = SubCompetitionDTO.get_dto(competition_game.sub_competition)
        home_team = CompetitionTeamDTO.get_dto(competition_game.home_team)
        away_team = CompetitionTeamDTO.get_dto(competition_game.away_team)
        rules = GameRulesDTO.get_dto(competition_game.rules)

        CompetitionGame.__init__(self, competition,
                                 sub_competition,
                                 competition_game.day,
                                 home_team,
                                 away_team,
                                 competition_game.home_score,
                                 competition_game.away_score,
                                 competition_game.complete,
                                 competition_game.processed,
                                 rules,
                                 competition_game.oid)
