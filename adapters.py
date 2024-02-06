"""Repositories module

TODO: Consider some refactoring and use of the protocol type for repos
"""

import slidow


class EventKeyValRepo:
    def __init__(self, kv_store: dict) -> None:
        if not "events" in kv_store:
            kv_store["events"] = {}
        self.kv_store = kv_store

    def add(self, event: slidow.Event) -> None:
        self.kv_store["events"][event.identifier] = event

    def get(self, event_id: str) -> slidow.Event:
        events = self.kv_store["events"]
        return events[event_id]


class QuizKeyValRepo:
    def __init__(self, kv_store: dict) -> None:
        if not "quizzes" in kv_store:
            kv_store["quizzes"] = {}
        self.kv_store = kv_store

    def add(self, quiz: slidow.Quiz) -> None:
        self.kv_store["quizzes"][quiz.identifier] = quiz

    def get(self, quiz_id: str) -> slidow.Quiz:
        quizzes = self.kv_store["quizzes"]
        return quizzes[quiz_id]
