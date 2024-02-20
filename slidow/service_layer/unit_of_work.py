"""Encapsulation of transaction boundaries"""

import abc

from slidow.adapters import repos


class AbstractUOW(abc.ABC):

    events: repos.AbstractRepo

    def __enter__(self) -> "AbstractUOW":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SQLAlchemyUOW(AbstractUOW):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.events = repos.EventSQLAlchemyRepo(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class DummyUOW(AbstractUOW):
    def __init__(self):
        self.events = repos.EventKeyValRepo({})
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self): ...
