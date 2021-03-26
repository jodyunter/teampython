from teams.data.dto.dto_game import GameDTO
from teams.domain.competition import CompetitionGame


class CompetitionGameDTO(GameDTO, CompetitionGame):

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