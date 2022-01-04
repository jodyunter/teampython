from abc import ABC, abstractmethod

from teams.data.database import Database
from teams.domain.utility.utility_classes import IDHelper
from teams.services.view_models import get_model


class BaseService(ABC):

    @abstractmethod
    def get_repo(self):
        pass

    def get_all(self, session=None):
        session = self.get_session(session)

        rules = self.get_repo().get_all(session)

        vms = [get_model.get_vm(r) for r in rules]

        return vms

    @staticmethod
    def get_new_id():
        return IDHelper.get_new_id()

    @staticmethod
    def get_session(session=None):
        if session is None:
            session = Database.get_session()

        return session

    @staticmethod
    def commit(session, commit):
        if commit:
            session.commit()
