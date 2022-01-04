from abc import ABC, abstractmethod

from teams.data.database import Database


class BaseTestService(ABC):

    @abstractmethod
    def test_create(self):
        pass

    @abstractmethod
    def test_get_all(self):
        pass

    @staticmethod
    def setup_test():
        Database.init_db("sqlite:///:memory:")
