"""The domain model"""

import typing
from dataclasses import dataclass


class Event:
    def __init__(self, identifier: str, name: str) -> None:
        self.identifier = identifier
        self.name = name
        self.quizzes : list['Quiz'] = []

    def __eq__(self, other) -> bool:
        if not isinstance(other, Event):
            return False
        return self.identifier == other.identifier


@dataclass
class Quiz:
    title: str
    questions: list["Question"] | None = None


@dataclass
class Question:
    text: str
    options: list["Option"] | None = None


@dataclass
class Option:
    text: str
    correct: bool = False
