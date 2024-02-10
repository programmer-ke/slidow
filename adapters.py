"""Repositories module

TODO: Consider some refactoring and use of the protocol type for repos
"""

import slidow


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


class EventKeyValRepo(KeyValRepo):
    table_name: str = "events"

    def add(self, event: slidow.Event) -> None:
        self._add(event.identifier, event)

    def get(self, event_id: str) -> slidow.Event:
        return self._get(event_id)


class QuizKeyValRepo(KeyValRepo):
    table_name: str = "quizzes"

    def add(self, quiz: slidow.Quiz) -> None:
        self._add(quiz.identifier, quiz)

    def get(self, quiz_id: str) -> slidow.Quiz:
        return self._get(quiz_id)


class EventSQLAlchemyRepo:

    def __init__(self, session) -> None:
        self.session = session

    def add(self, event: slidow.Event) -> None:
        self.session.add(event)

    def get(self, identifier: str) -> slidow.Event:
        return self.session.query(slidow.Event).filter_by(identifier=identifier).one()

class QuizSQLAlchemyRepo:

    def __init__(self, session) -> None:
        self.session = session

    def add(self, quiz: slidow.Quiz) -> None:
        self.session.add(quiz)

    def get(self, identifier: str) -> slidow.Quiz:
        return self.session.query(slidow.Quiz).filter_by(identifier=identifier).one()
