"""The domain model"""

import typing
from dataclasses import dataclass


@dataclass
class Event:
    name: str
    quiz: typing.Optional["Quiz"] = None

    def __eq__(self, other: 'Event'):
        return self is other


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
