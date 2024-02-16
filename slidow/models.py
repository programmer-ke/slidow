"""These are the slidow entities with related methods"""

import random
import string
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

    @classmethod
    def with_random_identifier(cls, event_name: str):
        """Return an event with a randomly generated identifier"""
        # todo: generate real randoms
        random_str = "".join([random.choice(string.ascii_letters) for _ in range(20)])
        return cls(random_str, event_name)


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
