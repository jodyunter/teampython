from unittest import TestCase

from teams.domain.utility.utility_classes import YearRestricted


class TestYearRestricted(TestCase):

    def test_should_pass_year_test_first_year(self):
        a = YearRestricted(5, 12)
        a.is_in_year(5)

    def test_should_pass_year_test_last_year(self):
        a = YearRestricted(5, 12)
        a.is_in_year(12)

    def test_should_pass_year_test_in_between_year(self):
        a = YearRestricted(5, 12)
        a.is_in_year(6)

    def test_should_not_pass_early(self):
        a = YearRestricted(5, 12)
        a.is_in_year(4)

    def test_should_not_pass_late(self):
        a = YearRestricted(5, 12)
        a.is_in_year(25)