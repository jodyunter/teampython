from unittest import TestCase

from teams.data.repo.controller_repository import ControllerRepository
from tests.teams.repo.test_base_repository import TestBaseRepository


class TestControllerRepository(TestBaseRepository, TestCase):
    repo = ControllerRepository()


