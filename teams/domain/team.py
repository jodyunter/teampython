from teams.domain.utility.utility_classes import IDHelper

# mapped
class Team:

    def __init__(self, name, skill, active, oid=None):
        self.name = name
        self.skill = skill
        self.active = active
        self.oid = IDHelper.get_id(oid)

