class YearRestricted:

    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year

    def is_in_year(self, year_to_check):
        return self.start_year <= year_to_check <= self.end_year