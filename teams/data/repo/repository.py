from abc import ABC, abstractmethod

from teams.data.database import Database


class Repository(ABC):

    @staticmethod
    def add(new_object, object_type, session):
        dto = object_type(new_object)
        session.add(dto)

    @staticmethod
    def get_session():
        return Database.get_session()

    @staticmethod
    def get_by_oid(oid, object_type, session):
        return session.query(object_type).filter_by(oid=oid).first()

    @staticmethod
    def get_all(object_type, session):
        return list(session.query(object_type).all())
