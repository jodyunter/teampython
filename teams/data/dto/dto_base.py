from sqlalchemy.ext.declarative import declarative_base

import abc
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


class DeclarativeABCMeta(DeclarativeMeta, abc.ABCMeta):
    pass


class Base(declarative_base(metaclass=DeclarativeABCMeta)):
    __abstract__ = True

# Base = declarative_base()
