from abc import ABC, abstractmethod

from teams.data.database import Database


class Repository(ABC):

    @abstractmethod
    def get_type(self):
        # this will give the default DTO object for the repository
        pass

    def add(self, new_object, session, object_type=None):
        if object_type is None:
            object_type = self.get_type()
        dto = object_type(new_object)
        session.add(dto)

    def get_session(self):
        return Database.get_session()

    def get_by_oid(self, oid,  session, object_type=None):
        if object_type is None:
            object_type = self.get_type()
        return session.query(object_type).filter_by(oid=oid).first()

    def get_all(self, session, object_type=None):
        if object_type is None:
            object_type = self.get_type()

        return list(session.query(object_type).all())


# this class can be used when you don't want a full repository object for a DTO
class BasicRepository(Repository):
    def get_type(self):
        return None
