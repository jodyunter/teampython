from abc import abstractmethod

from teams.data.database import Database


class BaseRepository:
    @abstractmethod
    def get_type(self):
        raise NotImplementedError

    @staticmethod
    def get_session():
        return Database.get_session()

    def get_by_oid(self, oid, session):
        return session.query(self.get_type()).filter_by(oid=oid).first()

    def get_all(self, session):
        return list(session.query(self.get_type()).all())
