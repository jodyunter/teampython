from abc import ABC

from teams.domain.game import Game
from teams.domain.record import Record


class Competition(ABC):

    def __init__(self, year, name, setup, started, complete):
        self.year = year
        self.name = name
        self.setup = setup
        self.started = started
        self.complete = complete


#  what rules do we need?
#  basic competition
class CompetitionRule(ABC):

    def __init__(self,  **kwargs):
        pass

