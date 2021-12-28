from abc import ABC, abstractmethod

from teams.data.database import Database


class Repository(ABC):

    def add(self, new_object, object_type, session):
        dto = object_type(new_object)
        session.add(dto)

    def get_session(self):
        return Database.get_session()

    def get_by_oid(self, oid, object_type, session):
        return session.query(object_type).filter_by(oid=oid).first()

    def get_all(self, object_type, session):
        return list(session.query(object_type).all())
