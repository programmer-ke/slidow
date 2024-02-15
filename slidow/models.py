"""These are the slidow entities with related methods"""

import typing
from dataclasses import dataclass, field


@dataclass
class Event:
    identifier: str
    name: str
    quizzes: list["Quiz"] = field(default_factory=list)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Event):
            return False
        return self.identifier == other.identifier


@dataclass
class Quiz:
    identifier: str
    title: str
    questions: list["Question"]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quiz):
            return False
        return self.identifier == other.identifier


@dataclass
class Question:
    text: str
    options: list["Option"]


@dataclass
class Option:
    text: str
    correct: bool = False
