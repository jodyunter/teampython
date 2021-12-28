from abc import ABC, abstractmethod
from unittest import TestCase

import pytest

from teams.data.database import Database
from teams.data.repo.repository import Repository
from teams.domain.utility.utility_classes import IDHelper


class BaseRepoTests(ABC):

    @abstractmethod
    def get_repo(self):
        pass

    @staticmethod
    def setup_database(connection="sqlite:///:memory:"):
        Database.init_db(connection)

    @staticmethod
    def setup_basic_test():
        BaseRepoTests.setup_database()
        session = Database.get_session()
        Database.clean_up_database(session)
        return session

    @staticmethod
    def get_id():
        return IDHelper.get_new_id()

    def test_add_record(self):
        session = self.setup_basic_test()
        record = self.get_add_record()
        self.get_repo().add(record, session, type(record))
        new_record = self.get_repo().get_by_oid(record.oid, session, type(record))
        self.assertEqual(record, new_record)

    def test_update_record(self):
        session = self.setup_basic_test()
        record = self.get_add_record()
        self.get_repo().add(record, session, type(record))
        session.commit()

        dto = self.get_repo().get_by_oid(record.oid, session, type(record))
        update_record = self.get_updated_record(dto)
        session.commit()

        dto = self.get_repo().get_by_oid(record.oid, session, type(record))

        self.assertEqual(dto, update_record)
        self.assertNotEqual(dto, record)

    @abstractmethod
    def get_add_record(self):
        pass

    @abstractmethod
    def get_updated_record(self, original_record):
        pass
