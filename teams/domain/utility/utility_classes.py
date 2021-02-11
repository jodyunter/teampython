import uuid


class IDHelper:

    @staticmethod
    def get_new_id():
        return str(uuid.uuid4())


class YearRestricted:

    def __init__(self, start_year, last_year):
        self.start_year = start_year
        self.last_year = last_year

    def is_in_year(self, year_to_check):
        return self.start_year <= year_to_check <= self.last_year

