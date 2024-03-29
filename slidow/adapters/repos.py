"""Aggregate repositories"""

import typing

from slidow import models


class AbstractRepo(typing.Protocol):
    def add(self, model: typing.Any) -> None: ...

    def get(self, id_: typing.Any) -> typing.Any: ...

    def list(self) -> typing.Any: ...


class KeyValRepo:
    table_name: str

    def __init__(self, kv_store: dict) -> None:
        if not self.table_name in kv_store:
            kv_store[self.table_name] = {}
        self.kv_store = kv_store

    def _add(self, key, val):
        self.kv_store[self.table_name][key] = val

    def _get(self, key):
        return self.kv_store[self.table_name][key]

    def _list(self):
        table = self.kv_store[self.table_name]
        return [table[key] for key in table]


class EventKeyValRepo(KeyValRepo, AbstractRepo):
    table_name: str = "events"

    def add(self, event: models.Event) -> None:
        self._add(event.identifier, event)

    def get(self, event_id: str) -> models.Event:
        return self._get(event_id)

    def list(self) -> typing.Iterable[models.Event]:
        return self._list()


class QuizKeyValRepo(KeyValRepo, AbstractRepo):
    table_name: str = "quizzes"

    def add(self, quiz: models.Quiz) -> None:
        self._add(quiz.identifier, quiz)

    def get(self, quiz_id: str) -> models.Quiz:
        return self._get(quiz_id)

    def list(self) -> typing.Iterable[models.Quiz]:
        return self._list()


class EventSQLAlchemyRepo(AbstractRepo):

    def __init__(self, session) -> None:
        self.session = session

    def add(self, event: models.Event) -> None:
        self.session.add(event)

    def get(self, identifier: str) -> models.Event:
        return self.session.query(models.Event).filter_by(identifier=identifier).one()

    def list(self) -> typing.Iterable[models.Event]:
        return self.session.query(models.Event).all()


class QuizSQLAlchemyRepo(AbstractRepo):

    def __init__(self, session) -> None:
        self.session = session

    def add(self, quiz: models.Quiz) -> None:
        self.session.add(quiz)

    def get(self, identifier: str) -> models.Quiz:
        return self.session.query(models.Quiz).filter_by(identifier=identifier).one()

    def list(self) -> typing.Iterable[models.Quiz]:
        return self.session.query(models.Quiz).all()
